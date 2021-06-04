import numpy as np
import pandas as pd
from typing import List
from sklearn.model_selection import train_test_split

def _stochastic_split(X, y):
    return train_test_split(X, y)

class Dataset():
    def __init__(self, name:str, path:str, y_name:str):
        """

        :param name:
        :param path:
        :param y_name: target column name.  X cols are all the other columns. [workaround]
        """

        self.path = path
        self.name = name
        self.y_name = y_name

        self.df = pd.read_csv(self.path)
        self.y = self.df[y_name]

        self.X = self.df.drop(y_name, axis = 1)

        self.X_val, self.X_test, self.y_val, self.y_test = _stochastic_split(self.X, self.y)



class ClassificationDatasets:

    fetal_health_dataset = Dataset(name="fetal",
                                   path="test_datasets/classification/fetal_health.csv",
                                   y_name="fetal_health")

    titanic_dataset = Dataset(name = "titanic",
                              path = "test_datasets/classification/titanic.csv",
                              y_name = "Survived")

    all_datasets_list = [
        fetal_health_dataset, titanic_dataset
    ]

    @staticmethod
    def get_list():
        return ClassificationDatasets.all_datasets_list