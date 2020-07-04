from sklearn.model_selection import train_test_split, cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from snorkel.analysis import metric_score
import numpy as np


class Classifier:
	"""
	A simple classification pipeline wrapping the `sklearn` library.

	- transforms (imputes, encodes/scales) categorical and numerical features
	- fits a classifier
	- computes accuracy scores for the classifier
	"""
	def __init__(self, num_features, cat_features, clf=RandomForestClassifier(n_estimators=100)):
		"""
		Initialize the pipeline.

		:param num_features: a list of df keys for the numerical features
		:param cat_features: a list of df keys for the categorical features
		:param clf: a classification (discriminative) model
		"""

		# categorical features are imputed with a constant and one-hot encoded
		cat_transformer = Pipeline([
			('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
			('oh_enc', OneHotEncoder(handle_unknown='ignore'))
		])
		# numerical features are imputed with the median and normalized
		num_transformer = Pipeline(steps=[
			('imputer', SimpleImputer(strategy='median')),
			('scaler', StandardScaler())
		])
		# a preprocessor for all the features, column by column
		self.preprocessor = ColumnTransformer(
			transformers=[
				('num', num_transformer, num_features),
				('cat', cat_transformer, cat_features)
			]
		)
		self.clf = self.get_clf(clf)

	def get_clf(self, model):
		"""
		Construct the pipeline - a feature preprocessor and a classification model.
		:param model: a classification (discriminative) model
		:return: a `sklearn` pipeline
		"""
		return Pipeline([
			('preprocessor', self.preprocessor),
			('classifier', model)
		])

	def fit(self, X, y):
		"""
		Fit the pipeline on a labeled dataset.
		:param X: the data
		:param y: the ground-truth labels
		:return: the fitted pipeline
		"""
		self.clf.fit(X, y)

	def score(self, X, y, verbose=True):
		"""
		Score the pipeline for accuracy on a test set.
		:param X: the test data
		:param y: ground-truth labels for the test data
		:param verbose: whether or not to print test accuracy
		:return: accuracy on the test set
		"""
		# calculate rounded predictions
		preds_test = np.round(self.clf.predict(X))
		# calculate the accuracy
		test_acc = metric_score(golds=y, preds=preds_test, metric="accuracy")
		if verbose:
			print(f"Test Accuracy: {test_acc * 100:.1f}%")
		return test_acc

	def cross_val(self, X, y, cv=5, verbose=True):
		"""
		Cross validate the pipeline.
		:param X: a dataset
		:param y: the ground-truth labels
		:param cv: number of folds in the cross validation
		:param verbose: whether or not to print test accuracy
		:return: the cross validation score object (`sklearn`)
		"""
		return cross_validate(self.clf, X, y, cv=cv, verbose=verbose)


def train_test_val_dev_split(X, y):
	"""
	Split the dataset into four partitions: training (64%), testing (16%), validation (16%), and development (4%).
	- Training is for fitting the model.
	- Testing is for testing the fitted model and parameter tuning.
	- Validation is for final testing after tuning parameters.
	- Development is for examining individual rows and performing unit tests.

	:param X: the dataset
	:param y: the ground-truth labels
	:return: four partitions of the dataset
	"""
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
	X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=1)
	X_test, X_dev, y_test, y_dev = train_test_split(X_test, y_test, test_size=0.2, random_state=1)
	return X_train, X_test, X_val, X_dev, y_train, y_test, y_val, y_dev