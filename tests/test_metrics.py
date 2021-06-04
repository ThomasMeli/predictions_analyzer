"""
Tests for metrics.py

"""
import pandas as pd
from tests.datasets_to_test import *
from predictions_analyzer.models import *
from predictions_analyzer.metrics import *

import numpy as np
import pandas as pd
from typing import List

def test_classification_models():
    all_models = AllClassificationModels()

    for model in all_models._get_models_list():
        pass



def test_ScikitModels():

    for dataset in ClassificationDatasets():

        print("\n")
        print(dataset.name)
        print(dataset.path)

        for model in AllClassificationModels():

            print("\n")
            print(model.name)
            model.fit(dataset.X_val, dataset.y_val)
            preds = model.predict(dataset.X_test)
            print(preds.shape)
            print(dataset.y_test.shape)

            model.report_speeds()

            classification_metrics = AllClassificationMetrics()

            for metric in classification_metrics:
                print(metric.name)
                the_score = metric.score(dataset.y_test, preds)
                print(the_score)


def test_AllRegressionModels():
    allreg = AllRegressionModels()
    print(allreg)

