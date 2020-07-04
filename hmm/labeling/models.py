from snorkel.labeling import PandasLFApplier
from snorkel.labeling import LabelModel
from snorkel.labeling import filter_unlabeled_dataframe
from snorkel.analysis import get_label_buckets
from snorkel.utils import probs_to_preds
import pandas as pd


class Labeler:
	"""
	Wrapper for Snorkel label model.

	- addition/change of labeling functions
	- label aggregation
	- model fitting
	- model evaluation: scoring and bucket analysis
	- filtering NAs
	"""
	def __init__(self, lfs=[], model=None):
		"""
		Instantiate the wrapper.
		:param lfs: list of labeling functions (heuristic functions)
		:param model: the model to use - by default, Snorkel's generative label model
		"""
		self.lfs = lfs
		self.applier = PandasLFApplier()
		self.model = LabelModel(cardinality=2, verbose=True) if model is None else model

	def add_lfs(self, lfs):
		"""
		Add labeling functions to the model.
		:param lfs: list of labeling functions to add
		"""
		self.lfs += lfs
		self.update_applier()

	def set_lfs(self, lfs):
		"""
		Set the list of labeling functions.
		:param lfs: labeling functions for the model
		"""
		self.lfs = lfs
		self.update_applier()

	def update_applier(self):
		"""
		Update the labeling function applier with the labeling functions. The applier is responsible for generating
		candidate labels for each tuple in the dataset, one set of candidate labels for each labeling function.
		"""
		self.applier = PandasLFApplier(lfs=self.lfs)

	def label(self, data, verbose=True):
		"""
		Aggregate candidate labels into a single label for each tuple in the dataframes in `data`.
		:param data: a set of dataframes, each containing a set of tuples to label
		:param verbose: whether or not to periodically print label status
		:return: a set of labels for each dataframe in `data`
		"""
		if isinstance(data, list):
			L = []
			for X in data:
				L.append(self._label_df(X, verbose))
			return L
		return self._label_df(data, verbose)

	def _label_df(self, X, verbose):
		"""
		Aggregate candidate labels into a single label for each tuple in the dataframes in `data`.
		:param X: a set of tuples to label
		:param verbose: whether or not to periodically print label status
		:return: labels for each tuple in `X`
		"""
		return self.applier.apply(df=X, progress_bar=verbose)

	def fit(self, L_train, Y_dev=None, fit_params={}):
		"""
		Fit the generative label model on a set of labels. No ground-truth labels are required for fitting, but can be
		included to help make the automatically generated label distribution match the ground-truth label distribution.
		Fitting involves only the candidate label distributions in the training set `L_train`.

		:param L_train: an `n` x `l` matrix of candidate labels, where `n` is the size of the training dataset and
		`l` is the number of labeling functions
		:param Y_dev: a held-out set of ground-truth labels
		:param fit_params: optional set of parameters for fitting - see Snorkel docs for all options
		:return: the fitted label model
		"""
		params = {'n_epochs': 500, 'lr': .001, 'log_freq': 100, 'seed': 1}
		params.update(fit_params)
		self.model.fit(L_train=L_train, Y_dev=Y_dev, **params)
		return self.model

	@staticmethod
	def score(model, L_valid, y_val, verbose=True):
		"""
		Validate the label model on a held out test set.

		:param model: a label aggregation model
		:param L_valid: an `n` x `l` matrix of candidate labels, where `n` is the size of the held-out validation set and
		`l` is the number of labeling functions
		:param y_val: ground-truth labels for the held-out validation set
		:param verbose: whether or not to periodically print label status
		:return:
		"""
		acc = model.score(L=L_valid, Y=y_val.values, tie_break_policy="random")["accuracy"]
		if verbose:
			print(f"{str(model)} {'Vote Accuracy:':<25} {acc*100:.1f}")
		return acc

	def get_preds(self, L, threshold=0.5):
		"""
		Produce rounded labels from a set of candidate labels produced for some dataset.

		:param L: an `n` x `l` matrix of candidate labels, where `n` is the size of the dataset and
		`l` is the number of labeling functions
		:param threshold: threshold for rounding posterior probabilities to discrete labels
		:return: the rounded labels
		"""
		probs_dev = self.model.predict_proba(L=L)
		return probs_dev >= threshold

	def get_label_buckets(self, L_dev, y_dev):
		"""
		Fetch a bucket of labels (i.a. false positives, false negatives)
		:param L_dev: an `n` x `l` matrix of candidate labels, where `n` is the size of the dev dataset and
		`l` is the number of labeling functions
		:param y_dev: ground truth labels for the dev set
		:return: a set of bucket labels - see the Moral Machine example for some analyses with label buckets
		"""
		preds_dev = self.get_preds(L_dev)
		return get_label_buckets(y_dev.values, preds_dev[:, 1])

	def get_confusion_matrix(self, L_dev, y_dev):
		"""
		Compute the confusion matrix for the final labels for a held out development set.
		:param L_dev: an `n` x `l` matrix of candidate labels, where `n` is the size of the dev dataset and
		`l` is the number of labeling functions
		:param y_dev: ground truth labels for the dev set
		:return: the confusion matrix as a pandas crosstab
		"""
		preds_dev = self.get_preds(L_dev)
		return pd.crosstab(y_dev.values.astype(bool), preds_dev[:, 1], rownames=['Actual'], colnames=['Predicted'])

	def filter_probs(self, X, L):
		"""
		Filter unlabeled rows (where all the labeling functions abstain) from the dataset.
		:param X: the dataset
		:param L:a n `n` x `l` matrix of candidate labels, where `n` is the size of the dataset and
		`l` is the number of labeling functions
		:return: the dataset with any unlabeled tuples removed
		"""
		return filter_unlabeled_dataframe(
			X=X, y=self.model.predict_proba(L=L), L=L
		)

	@staticmethod
	def probs_to_preds(probs):
		return probs_to_preds(probs=probs)
