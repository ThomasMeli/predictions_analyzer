
class Metric:
    """
    Base metric class.

    """
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
    pass


# Creating the Report
class Report:
    """Base class for metric reporting"""
    pass

class RegressionReport:
    pass

class ClassificationReport:
    pass
