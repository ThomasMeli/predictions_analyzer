from tests.datasets_to_test import *


def test_classification_dataset_list():
    datasets = ClassificationDatasets()
    print(datasets)

    for dataset in datasets:
        print("\n")
        print(dataset.name)
        print(dataset.path)
        print(dataset.X.shape)
        print(dataset.y.shape)