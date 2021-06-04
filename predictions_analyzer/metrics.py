from sklearn.metrics import accuracy_score, auc, roc_auc_score

class Metric:
    """
    Base metric class.

    """
    def __init__(self, metric_object,
                 name:str = "",):
        self.name = name
        self.metric_object = metric_object

    def score(self, y_true, y_pred):
        self.value = self.metric_object(y_true, y_pred)
        return self.value


class RegressionMetric(Metric):
    pass

class ClassificationMetric(Metric):
    pass

class MetricInterface:
    """
    Deals with implementation of each metric.
    Has opportunities to LOG or integrate with WANDB or other integrations.

    """
    pass


# Classes containing Aggregates of Metric Objects.
class AllRegressionMetrics():
    pass

class AllClassificationMetrics():
    def __init__(self):
        self.accuracy_score = Metric(name = "accuracy",
                                     metric_object=accuracy_score)

        self.metrics = self._get_classigication_metrics()

    def _get_classigication_metrics(self):
        return [
            self.accuracy_score
        ]

    def __getitem__(self, item):
        return self.metrics[item]

# Creating the Report
class Report:
    """Base class for metric reporting"""
    pass

class RegressionReport:
    pass

class ClassificationReport:
    pass
