"""
Tests for models.py

"""
import pandas as pd
from tests.datasets_to_test import *

from predictions_analyzer.models import *

import numpy as np
import pandas as pd
from typing import List

from sklearn.linear_model import Lasso

def test_classification_models():
    all_models = AllClassificationModels()

    for model in all_models.get_models_list():
        pass



def test_ScikitModels():
    my_lasso = ScikitModel(Lasso())

    # Todo: .get_list will be depreciated in favor of an iterable class.

    for dataset in ClassificationDatasets.get_list():

        print("\n")
        print(dataset.name)
        print(dataset.path)

        # Todo: .get_models_list will be depreciated in favor of an iterable class.
        for model in AllClassificationModels().get_models_list():

            print("\n")
            print(model.name)
            model.fit(dataset.X_val, dataset.y_val)
            preds = model.predict(dataset.X_test)

            print(preds.shape)

            model.report_speeds()

def test_AllRegressionModels():
    allreg = AllRegressionModels()
    print(allreg)

