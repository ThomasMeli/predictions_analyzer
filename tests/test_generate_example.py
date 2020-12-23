
from src.generate_example import *

def test_validate_classification_constructor():

    X, y = get_classification()

    assert 1 + 1 == 2

def test_ExampleAnalyzerConstructor():
    assert ExampleClassificationAnalyzer()

def test_fit():
    ex = ExampleClassificationAnalyzer()

    ex.fit()
    ex.predict()

    print(ex.preds_df)
    print(ex.preds_df.shape)


