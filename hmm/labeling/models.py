from snorkel.labeling import PandasLFApplier
from snorkel.labeling import LabelModel
from snorkel.labeling import filter_unlabeled_dataframe
from snorkel.analysis import get_label_buckets
from snorkel.utils import probs_to_preds
import pandas as pd

class Labeler:
	def __init__(self, lfs=[]):
		self.lfs = lfs
		self.applier = PandasLFApplier(lfs=self.lfs)
		self.model = LabelModel(cardinality=2, verbose=True)

	def add_lfs(self, lfs):
		self.lfs += lfs
		self.update_applier(self.lfs)

	def set_lfs(self, lfs):
		self.lfs = lfs
		self.update_applier(self.lfs)

	def update_applier(self, lfs):
		self.applier = PandasLFApplier(lfs=self.lfs)

	def label(self, data, verbose=True):
		if isinstance(data, list):
			L = []
			for X in data:
				L.append(self._label_df(X, verbose))
			return L
		return self._label_df(data, verbose)

	def _label_df(self, X, verbose):
		return self.applier.apply(df=X, progress_bar=verbose)

	def fit(self, L_train, Y_dev=None, fit_params={}):
		params = {'n_epochs': 500, 'lr': .001, 'log_freq': 100, 'seed': 1}
		params.update(fit_params)
		self.model.fit(L_train=L_train, Y_dev=Y_dev, **params)
		return self.model

	@staticmethod
	def score(model, L_valid, y_val, verbose=True):
		acc = model.score(L=L_valid, Y=y_val.values, tie_break_policy="random")["accuracy"]
		if verbose: print(f"{str(model)} {'Vote Accuracy:':<25} {acc*100:.1f}")
		return acc

	def get_preds(self, L_dev, y_dev):
		threshold = 0.5
		probs_dev = self.model.predict_proba(L=L_dev)
		return probs_dev >= threshold

	def get_label_buckets(self, L_dev, y_dev):
		preds_dev = self.get_preds(L_dev, y_dev)
		return get_label_buckets(y_dev.values, preds_dev[:, 1])

	def get_confusion_matrix(self, L_dev, y_dev):
		preds_dev = self.get_preds(L_dev, y_dev)
		return pd.crosstab(y_dev.values.astype(bool), preds_dev[:, 1], rownames=['Actual'], colnames=['Predicted'])

	def filter_probs(self, X, L):
		return filter_unlabeled_dataframe(
			X=X, y=self.model.predict_proba(L=L), L=L
		)

	@staticmethod
	def probs_to_preds(probs):
		return probs_to_preds(probs=probs)
