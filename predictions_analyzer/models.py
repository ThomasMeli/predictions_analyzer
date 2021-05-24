"""
Base classes for models to declutter other code

These can be sub-builders that contribute to what models are used.

"""

class Model:
    """
    Base class to all models
    """

    # Name.
    # Category of Problem (classification, regression, other).
    # Estimator Object.
    # API (Scikit, Keras, PyTorch, XGB, etc.)

    pass

class ScikitModel(Model):


    pass

class XGBModel(Model):
    pass

class KerasModel(Model):
    pass

class TrainInterface:
    """
    Training interface (.fit() method for most estimators).
    Handles custom XGBoost .train() API for custom training.
    Extensible with other model types.

    """
    pass



# Model Aggregations to loop through.

class BaseClassificationModels:
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

#
class SKLinearRegression(ScikitModel):
    pass



class AllRegressionModels:

    # SKLinearRegression
    pass
