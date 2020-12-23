
from src.generate_example import *
from sklearn.metrics import accuracy_score

def get_ExClfObj():
    ex = ExampleClassificationAnalyzer()

    ex.fit()
    ex.predict()

    return ex

def test_apply_ytrue():
    ex = get_ExClfObj()

    accuracy = ex.apply_ytrue(func = accuracy_score,
                                 func_name = "accuracy_score",
                                 df = ex.preds_df)
    print(accuracy)
    print(accuracy.shape)

def test_add_to_metrics_from_ytrue_and_preds_df():
    ex = get_ExClfObj()
    ex.add_to_metrics_from_ytrue_and_preds_df(func = accuracy_score,
                                              func_name = "accuracy_score")

    print(ex.metrics_df)

    assert ex.metrics_df.empty != True  # Assert dataframe is not empty.


def test_validate_classification_constructor():

    X, y = get_classification()

    assert 1 + 1 == 2

def test_ExampleAnalyzerConstructor():
    assert ExampleClassificationAnalyzer()

def test_fit_predict():
    ex = ExampleClassificationAnalyzer()

    ex.fit()
    ex.predict()

    print(ex.preds_df)
    print(ex.preds_df.shape)

def test_fit_class_metrics():
    ex = ExampleClassificationAnalyzer()

    ex.fit()
    ex.predict()
    ex.get_classification_metrics()

    print(ex.metrics_df)



