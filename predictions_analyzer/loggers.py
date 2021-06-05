"""
Observer Pattern?

"""

class LoggingEvent:
    """
    Use this class to encapsulate log points.
    Speed, memory usage, etc.



    """
    pass

class LoggingEventHandler():
    """
    This is the class that handles the logging
    events, depending on what service
    one is using.

    You can add a custom function or class
    that runs as well at each log point.

    """
    def __init__(self):
        pass

    def at_event_run_funct(self, func):
        pass

    pass

class DataLogger:
    """
    Logs Data Information.
    Shape
    Memory
    """
    pass

class ModelLogger:
    """
    Logs Model hyperparameters but not
    the model itself unless specified.

    """

class ModelPerformanceLogger:
    pass
