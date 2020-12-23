"""
Generates examples of dfs to play around with
"""

import sklearn.datasets
import sklearn.linear_model
import sklearn.tree
import sklearn.ensemble

import pandas as pd
from src.analyze import Analyzer

def get_classification():
    X, y = sklearn.datasets.make_classification(
        n_classes = 5,
        n_features = 20,
        n_informative = 15,
        n_redundant = 5,
        n_clusters_per_class = 3
    )

    # For logging
    print(X.shape)
    print(y.shape)

    return X, y

class BaseClassificationAnalyzer:
    pass

class BaseRegressionAnalyzer:
    pass

class ExampleClassificationAnalyzer:
    def __init__(self):

        self.X, self.y = get_classification()
        self.is_fit = False

        self.y_true = self.y

        self.linreg = sklearn.linear_model.LinearRegression()
        self.lasso = sklearn.linear_model.Lasso()
        self.ridge = sklearn.linear_model.Ridge()
        self.dec_tree = sklearn.tree.DecisionTreeClassifier()
        self.extr_tree = sklearn.ensemble.ExtraTreesClassifier()
        self.random_forest = sklearn.ensemble.RandomForestClassifier()
        self.bagging_clf = sklearn.ensemble.BaggingClassifier()

        # A list of named tuples of all models to loop through.
        self.models = [
            (self.linreg, "linreg"),
            (self.lasso, "lasso"),
            (self.ridge, "ridge"),
            (self.dec_tree, "dec_tree"),
            (self.random_forest, "random_forest"),
            (self.extr_tree, "extr_tree"),
            (self.bagging_clf, "bagging_clf")
                    ]


    def _set_is_fit(self, is_it_fit: bool):
        """
        Sets if the estimators are fit or not
        :return:
        """

        self.is_fit = is_it_fit

    def _is_fit(self):
        """
        TO DO - Make This Private

        find if the models are fit or not.
        This can be updated if there is a better method.
        :return:
        """

        if self.is_fit == False:
            return False
        if self.is_fit == True:
            return True

    def fit(self):
        """
        Fit all the base models.
        :return:
        """

        for model, model_name in self.models:
            model.fit(self.X, self.y)

        self.is_fit = self._set_is_fit(True)

    def predict(self):

        # Here or in the __init__?
        self.preds_df = pd.DataFrame(self.y_true, columns = ["y_true"])

        for model, model_name in self.models:
            self.preds_df[model_name] = model.predict(self.X)

        return self.preds_df

    def within_threshold(self, threshold: float):
        """
        Finds all
        :param threshold: float - Find all outputs that are within a threshold.

        :return:
        """

        # Validate that the model is fit already.

    def get_classification_metrics(self):
        pass

    def analyze(self):
        pass

    def analyze_ensemble(self):
        pass

    def fit_ensemble(self):
        """

        :return:
        """
        pass

    def fit_null_test(self):
        """
        Create random predictions in a certain range
        and see how that compares with your other
        models.

        :return:
        """
        pass

    def fit_random_seed_variance(self):
        """
        How much variance is there in just changing the random seed
        :return:
        """
        pass

    def correlated_predictions(self):
        """
        Get diverse predictors by finding uncorrelated predictions.

        :return:
        """
        pass

    def bootstrap(self):
        pass


