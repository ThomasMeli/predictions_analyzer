"""
An ensemble analysis.
"""

class BaseEnsembleAnalyzer()
    def __init__(self):
        self.submissions = []

class RegressionEnsembleAnalyzer(BaseEnsembleAnalyzer):
    def __init__(self):
        self.submissions = []

    def add_csvs(self, dfs):
        pass

    def add_csv(self, df):
        pass

    def most_similar_predictions(self):
        pass

    def most_different_predictions(self):
        pass

    def analyze(self):
        pass

class MultiOutRegressionEnsembleAnalyzer(BaseEnsembleAnalyzer)
    def __init__(self):
        self.submissions = []

