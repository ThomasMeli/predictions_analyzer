"""
Base classes for models to declutter other code

These can be sub-builders that contribute to what models are used.

Create interfaces for different APIs and different capacities.

Fitable, Predictable, MultiOutputable
Classifiable, Regressable, Kerasable,
PyTorchable,
"""

from predictions_analyzer.metrics import *

from collections import MutableSequence
from sklearn.linear_model import Lasso

import sklearn.dummy
import sklearn.datasets
import sklearn.linear_model

from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.tree import ExtraTreeClassifier, ExtraTreeRegressor

from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor, BaggingClassifier, BaggingRegressor
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, GradientBoostingRegressor, RandomForestRegressor


import sklearn.ensemble
import sklearn.naive_bayes
import sklearn.neighbors

from time import time

class Model:
    """
    Base class to all models
    """

    # Name.
    # Category of Problem (classification, regression, other).
    # Estimator Object.
    # API (Scikit, Keras, PyTorch, XGB, etc.)

    model_type = None  # sklearn, keras, xgb, etc.
    has_cv = False  # Does it have an autoCV?
    single_input = True  # Single input or multi-input
    single_output = True  # Single output or multi-output
    optuna_integration = False  # Does it have a custom optuna integration.

    # Should you do a def __init__ on this as a base class?
    # like self.model_object?  Here?

class ScikitModel(Model):

    model_type = "scikit"

    def __init__(self, model_object, name = ""):
        self.name = name
        self.model_object = model_object

    def __str__(self):
        return str(str(id(self.model_object)), self.model_type)

    def __repr__(self):
        return str(self.model_object)

    def fit(self, X, y):
        # Add Memory + Space Measuring

        fit_start_time = time()
        fitted_obj = self.model_object.fit(X, y)
        fit_end_time = time()

        self.fit_duration = fit_end_time - fit_start_time

        return fitted_obj

    def predict(self, X):
        # Add Memory + Space Measuring

        pred_start_time = time()
        self.predictions = self.model_object.predict(X)
        pred_end_time = time()

        self.pred_duration = pred_end_time - pred_start_time

        return self.predictions

    def report_speeds(self):
        print("Time to fit: ", round(self.fit_duration, 5), "seconds")
        print("Time to predict: ", round(self.pred_duration, 5), "seconds")

class XGBModel(Model):

    model_type = "xgb"


    pass

class KerasModel(Model):
    model_type = "keras"

    pass

class TrainInterface:
    """
    Training interface (.fit() method for most estimators).
    Handles custom XGBoost .train() API for custom training.
    Extensible with other model types.

    """
    pass


# Model Aggregations to loop through.

class ModelAggregator:
    """
    This class will create a sequence like object
    of a list of Models

    """

    @staticmethod
    def aggregate_model_objects(list_of_Models):
        """

        :param list_of_Models: A list object containing
        Model objects.

        :return:
        """

        pass

class BaseClassificationModels:
    """
    Thinking: Overloads the + and -
    for easy appending and deleting.

    Perhaps you can sort them along some
    criteria as well - by speed, by accuracy,
    by whatever metric you want.

    """
    pass

class BaseClassificationModelsMulti:
    pass

class BaseClassificationModelsTabNN:
    pass

# Aggregation of Regression Models

class SingleOutputRegressionModels:
    pass

class MultiOutputRegressionModels:
    pass

class MultiOutputWrapper:
    pass

class SKLinearRegression(ScikitModel):
    pass

# MutableSequence Like
class BaseAllModels:
    def __init__(self):
        self.models = []

    #def __str__(self):
    #    return str()

    def __iadd__(self, other):
        return self.models.append(other)

    def __add__(self, other):
        return self.models.append(other)

    def __getitem__(self, item):
        return self.models[item]

    #def __setitem__(self, item):
    #    pass

    #def __delitem__(self, key):
    #    pass

    def __len__(self):
        return len(self.models)

# MutableSequence
class AllClassificationModels(BaseAllModels):

    def __init__(self):

        self.decision_tree = ScikitModel(DecisionTreeClassifier(), name = "Decision Tree")
        self.extra_tree = ScikitModel(ExtraTreeClassifier(), name = "Extra Trees")
        self.adaboost = ScikitModel(AdaBoostClassifier(), name = "AdaBoost")
        self.bagging = ScikitModel(BaggingClassifier(), name = "BaggingTree")
        self.gradboost = ScikitModel(GradientBoostingClassifier(), name = "GradBoost")
        self.randomforest = ScikitModel(RandomForestClassifier(), name = "Random Forest")

        self.models = self._get_models_list()

    # Todo: ._get_models_list will be depreciated in favor of an iterable class.
    def _get_models_list(self):

        return [
            self.decision_tree,
            self.extra_tree,
            self.adaboost,
            self.bagging,
            self.gradboost,
            self.randomforest,
        ]





class AllDummyClassifications(BaseAllModels):
    pass

# MutableSequence
class AllRegressionModels(BaseAllModels):
    # SKLinearRegression

    def __init__(self):
        self.decision_tree = ScikitModel(DecisionTreeRegressor(), name="Decision Tree")
        self.extra_tree = ScikitModel(ExtraTreeRegressor(), name="Extra Trees")
        self.adaboost = ScikitModel(AdaBoostRegressor(), name="AdaBoost")
        self.bagging = ScikitModel(BaggingRegressor(), name="BaggingTree")
        self.gradboost = ScikitModel(GradientBoostingRegressor(), name="GradBoost")
        self.randomforest = ScikitModel(RandomForestRegressor(), name="Random Forest")


class AllDummyRegressions():
    pass

