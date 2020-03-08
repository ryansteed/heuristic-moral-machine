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
	def __init__(self, features, num_features, cat_features, clf=RandomForestClassifier(n_estimators=100)):
		cat_transformer = Pipeline([
			('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
			('oh_enc', OneHotEncoder(handle_unknown='ignore'))
		])
		num_transformer = Pipeline(steps=[
			('imputer', SimpleImputer(strategy='median')),
			('scaler', StandardScaler())
		])
		self.preprocessor = ColumnTransformer(
		    transformers=[
				('num', num_transformer, num_features),
				('cat', cat_transformer, cat_features)
		    ]
		)
		self.clf = self.get_clf(clf)

	def get_clf(self, model):
		return Pipeline([
			('preprocessor', self.preprocessor),
			('classifier', model)
		])

	def fit(self, X, y):
		self.clf.fit(X, y)

	def score(self, X, y, verbose=True):
		preds_test_dev = np.round(self.clf.predict(X))
		test_acc = metric_score(golds=y, preds=preds_test_dev, metric="accuracy")
		if verbose: print(f"Test Accuracy: {test_acc * 100:.1f}%")
		return test_acc
    
#     def cross_val(self, X, y, cv=5, verbose=True):
#         return cross_validate(self.clf, X, y, cv=cv, verbose=verbose)


def train_test_val_dev_split(X, y):
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
	X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=1)
	X_test, X_dev, y_test, y_dev = train_test_split(X_test, y_test, test_size=0.2, random_state=1)
	return X_train, X_test, X_val, X_dev, y_train, y_test, y_val, y_dev