"""
Facade Object for total project.

"""

from predictions_analyzer.models import *
from predictions_analyzer.metrics import *

class BaseProject:
    pass

class ClassificationProject:
    self.models = AllClassificationModels
    self.metrics = AllClassificationMetrics

    pass

class RegressionProject:
    self.models = AllRegressionModels
    self.metrics = AllRegressionMetrics


