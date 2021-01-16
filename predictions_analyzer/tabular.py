"""
For Tabular_ML Predictions.

This serves to simulate the data and API of the tabular_prediction_analyzer.

For now, it is the main module for the tabular ML analyzer and just
serves as an example of what is possible.

Should inherit a Base Class Analyzer in the future that users can
use with real numpy or pandas data.

"""
from tqdm import tqdm
from time import time

from lightgbm import LGBMClassifier
import xgboost as xgb

import sklearn.dummy
import sklearn.datasets
import sklearn.linear_model
import sklearn.tree
import sklearn.ensemble
import sklearn.metrics
from sklearn.metrics import plot_confusion_matrix, classification_report
import sklearn.model_selection

import sklearn.naive_bayes
import sklearn.neighbors

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from predictions_analyzer.analyze import Analyzer

from itertools import combinations

def get_classification(random_state = 42):
    """
    Creates a classification dataset.
    Wrapper for sklearn's make_classification.

    :param random_state: Specifies a random seed
    :return: A tuple of X,y values.
    """
    X, y = sklearn.datasets.make_classification(
        n_samples = 1000,
        n_classes = 5,
        n_features = 20,
        n_informative = 5,
        n_redundant = 15,
        n_clusters_per_class = 3,
        random_state = random_state
    )

    # For logging
    print(X.shape)
    print(y.shape)

    return X, y

class BaseAnalyzer:
    """
    Contains methods common to both regression and classification
    analyzers.

    """

    def show_models(self):
        for model in self.models:
            print("\n")
            print(model)

    def remove_model(self):
        """

        :return:
        """
        pass

    def update_model(self):
        pass

    def add_model(self, model_name:str, model_object):
        """
        Adds a model
        :param model_name: classifier_name
        :param model_obj: classifier object with .fit and .predict methods
        :return:

        """

        # Is this possible?
        # self.model_name = model_object

        self.models.append((model_object, model_name))

    def add_models(self):
        """
        Plural version of add_model
        Eventually refactor into one function

        :return:

        """
        pass

    def remove_all_models(self):
        pass

    def restore_baseline_models(self):
        self._initialize_models()

    def _initialize_preds(self):
        self.ensembled_preds_df = pd.DataFrame()

        # This will be the original_preds & ensembled_preds
        self.all_preds_df = pd.DataFrame()

    def _set_is_fit(self, is_it_fit: bool):
        """
        Sets if the estimators are fit_models or not
        :return:
        """

        self.is_fit = is_it_fit

    def _is_fit(self):
        """
        TO DO - Make This Private

        find if the models are fit_models or not.
        This can be updated if there is a better method.
        :return:
        """

        if self.is_fit == False:
            return False
        if self.is_fit == True:
            return True

    def load_unsplit_data(self, X, y):
        self.X = X
        self.y = y

    def load_split_data(self, X_train, y_train,
                        X_valid, y_valid):

        self.X_train = X_train
        self.y_train = y_train
        self.X_valid = X_valid
        self.y_valid = y_valid

    def fit_models(self, verbose = True):
        """
        Fit all models on the self.X_train and self.y_train data.
        Should only be used if you don't already have
        offline predictions done already.

        :return:
        """

        self.model_fit_speeds = pd.DataFrame()

        for model, model_name in self.models:

            time_start = time()

            model.fit(self.X_train, self.y_train)

            time_finish = time()
            time_to_fit = round(time_finish - time_start, 4)

            if verbose:
                print("fit:", model_name, time_to_fit, "seconds")

            self.model_fit_speeds[model_name] = time_to_fit


        self.is_fit = self._set_is_fit(True)

    def predict(self, verbose = True):
        """
        Predict on the self.X_valid and self.y_valid and save time metrics.
        Must run or load a validation split and .fit_models first.

        :param verbose:
        :return:
        """

        # Here or in the __init__?
        self.preds_df = pd.DataFrame(self.y_true, columns = ["y_true"])

        # TODO: Check if model split_val_train has been called

        self.model_pred_speeds = pd.DataFrame()

        for model, model_name in self.models:

            time_start = time()

            # TODO: Add Exception handling to predict doesn't stop.

            self.preds_df[model_name] = model.predict(self.X_valid)

            time_finish = time()
            time_to_fit = round(time_finish - time_start, 4)

            if verbose:
                print("predicted with:", model_name, "took ", time_to_fit, "seconds")

            self.model_pred_speeds[model_name] = time_to_fit

        # Drop y_true.  Just keep it in self.y_true
        self.preds_df = self.preds_df.drop("y_true", axis = 1)

        return self.preds_df

    def apply_ytrue(self,
                       func,
                       df: pd.DataFrame = None,
                       func_name: str = None,):
        """
        TO UPDATE: Should be private function

        Applies func(y_true, col in cols...) across dataframe df

        Helper function to use df.apply with
        self.preds_df and self.y_true

        func - the function being passed to apply
        across columns.  func should take self.y_true
        as its first argument.

        df - the df to apply the func to.

        :return: a df or series with the result.
        """

        # How to get this to work with pd.apply when there is varying
        # positional arguments?  args = () ?

        if df is None:
            df = self.preds_df

        applied_df = pd.DataFrame(columns = df.columns,
                                  index = [func_name])

        for col in df.columns:
            applied_df[col] = func(self.y_true, df[col])

        return applied_df

    def add_to_metrics_from_ytrue_and_preds_df(self,
                                               func,
                                               func_name: str = None):
        """

        Helper wrapper function to apply_ytrue
        encapsulate any future
        changes to apply_ytrue or the
        preds_df structure

        :return:
        """

        # FIX: apply_ytrue should be private function
        # Modularize this.
        ### DRY Violated

        new_metric = self.apply_ytrue(func = func,
                                      df = self.preds_df,
                                      func_name = func_name)

        assert new_metric.empty != True  # Was the new_metric created?

        # Encapsulate this in a new private function
        self.metrics_df = pd.concat([self.metrics_df, new_metric])
        assert self.metrics_df.empty != True  # Has metric been added to self.metrics_df?


        ########### Do the same for Ensembled Preds ###################
        # Modularize this
        # If ensembled predictions have been created...
        if self.ensembled_preds_df.empty != True:
            new_ensembled_metric = self.apply_ytrue(func = func,
                                                    df=self.ensembled_preds_df,
                                                    func_name=func_name)

            self.metrics_df = pd.concat([self.metrics_df, new_ensembled_metric])

            assert self.metrics_df.empty != True  # Has metric been added to self.metrics_df?


class BaseClassificationAnalyzer(BaseAnalyzer):
    """
    Base class for all Classification Analyzers

    """

    def _initialize_models(self):
        self.dummy = sklearn.dummy.DummyClassifier(strategy="prior")

        # Set random state / seeds for these

        self.logistic_reg = sklearn.linear_model.LogisticRegression(penalty="none",
                                                                    n_jobs=self.n_jobs)

        self.logistic_l1 = sklearn.linear_model.LogisticRegression(penalty="l1",
                                                                   solver="saga",
                                                                   n_jobs=self.n_jobs)

        self.logistic_l2 = sklearn.linear_model.LogisticRegression(penalty="l2",
                                                                   solver="saga",
                                                                   n_jobs=self.n_jobs)

        self.logistic_elastic = sklearn.linear_model.LogisticRegression(penalty="elasticnet",
                                                                        solver="saga",
                                                                        n_jobs=self.n_jobs)

        self.ridge = sklearn.linear_model.RidgeClassifier(normalize=True)

        self.svc = sklearn.svm.SVC()

        self.nb = sklearn.naive_bayes.GaussianNB()
        self.nb_complement = sklearn.naive_bayes.ComplementNB()

        self.knn = sklearn.neighbors.KNeighborsClassifier()

        self.dec_tree = sklearn.tree.DecisionTreeClassifier(max_depth=self.max_depth)
        self.extr_tree = sklearn.ensemble.ExtraTreesClassifier(max_depth=self.max_depth)
        self.random_forest = sklearn.ensemble.RandomForestClassifier(max_depth=self.max_depth)
        self.bagging_clf = sklearn.ensemble.BaggingClassifier(max_features=0.8,
                                                              max_samples=self.use_subsample)

        self.xgb_clf = xgb.XGBClassifier(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            subsample=self.use_subsample,
            tree_method="approx"
        )

        self.lgb_clf = LGBMClassifier(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            num_leaves=64
        )

        # TODO: Organize into model types so each model can .fit on data made for it.
        # Logistic, Linear classifiers. SVC. KNN.
        self.models_that_need_scaled_data = []

        self.tree_based_models = []

        # Don't use these with big-data.   KNN or SVC.
        self.models_that_dont_scale_well = [
            (self.svc, "SVC"),
            (self.knn, "knn"),
            (self.random_forest, "random_forest")
        ]

        # A list of named tuples of all models to loop through.
        self.models = [
            (self.dummy, "dummy_prior_clf"),
            (self.logistic_reg, "logistic_reg"),
            (self.logistic_l1, "logistic_l1"),
            (self.logistic_l2, "logistic_l2"),
            (self.ridge, "ridge"),
            (self.nb, "nb"),
            (self.dec_tree, "dec_tree"),
            (self.extr_tree, "extr_tree"),
            (self.bagging_clf, "bagging_clf"),
            (self.xgb_clf, "xgb_clf"),
            (self.lgb_clf, "lgb_clf")
        ]

    def _initialize_metrics(self):

        self.metrics_df = pd.DataFrame()
        self.accuracy = []  # List of accuracy scores?

        self.binary_metrics = [
            (sklearn.metrics.accuracy_score, "accuracy_score"),
            (sklearn.metrics.roc_auc_score, "roc_auc_score")
        ]

        self.binary_or_multiclass_metrics = [
            (sklearn.metrics.precision_score, "precision_score"),
            (sklearn.metrics.recall_score, "recall_score"),
            (sklearn.metrics.f1_score, "f1_score"),
            (sklearn.metrics.log_loss, "log_loss")

        ]

    def generate_data(self):
        X, y = get_classification(random_state=self.random_state)
        X = pd.DataFrame(X)
        y = pd.DataFrame(y)

        # TODO: Delete this to not duplicate data.  Just deal with train/val splits.
        self.X = X
        self.y = y

        self.split_val_train()

class BaseRegressionAnalyzer(BaseAnalyzer):
    pass

class ClassificationAnalyzer(BaseClassificationAnalyzer):
    """
    FITTING
    PREDICTING
    ANALYZING should be clearly differentiated and encapsulated things.

    """

    def __init__(self,
                 random_state = 42,
                 max_depth = 5,
                 n_estimators = 100,
                 use_subsample = 0.8,
                 n_jobs = -1,
                 simulate_data = False):

        self.random_state = random_state

        self.n_estimators = n_estimators
        self.use_subsample = use_subsample

        self.max_depth = max_depth
        self.is_fit = False
        self.n_jobs = n_jobs

        self._initialize_models()
        self._initialize_metrics()
        self._initialize_preds()

        if simulate_data:
            self.generate_data()


    def _update_validation_ready_models(self):
        """
        Models with early stopping should include validation sets.

        :return:
        """
        pass

    def split_val_train(self,
                        train_fraction = 4/5,
                        method = "stochastic",
                        verbose = True):
        """
        Splits data into train and validation splits.
        Useful for quick processing.

        :param X:
        :param y:
        :param: method ("stochastic", "time_series")
        :return:
        """

        X = self.X
        y = self.y

        length_of_X = len(X)

        if method == "stochastic":
            self.X_train, self.X_valid, self.y_train, self.y_valid = sklearn.model_selection.train_test_split(
                X, y, train_size = train_fraction,
                stratify = y,
                random_state=self.random_state,
                shuffle = True
            )

        if method == "time_series":
            # TODO: Add stochastic and time-series variants.

            split_at_id = int(length_of_X * train_fraction)

            self.X_train = X.iloc[0:split_at_id, :]
            self.y_train = y.iloc[0:split_at_id]

            self.X_valid = X.iloc[split_at_id:, :]
            self.y_valid = y.iloc[split_at_id:]

        self.y_true = self.y_valid
        self._update_validation_ready_models()

    def cross_validate(self):
        pass




    def load_preds(self):
        pass


    def within_threshold(self, threshold: float):
        """
        Finds all
        :param threshold: float - Find all outputs that are within a threshold.

        :return:
        """

        # Validate that the model is fit_models already.





    def show_preds_report(self, save = False):
        """
        Show pandas styled dataframe with reds -> incorrect, greens -> correct.

        Sort by number incorrect. / TODO: customize show features.

        Classification Report for Each Classifier.

        :param save: Save outputs to a filepath.

        :return:
        """
        pass


    def show_confusion_matrix(self, verbose = True):

        for model, model_name in tqdm(self.models):

            # TODO: Add Exception handling to predict doesn't stop.

            disp = plot_confusion_matrix(model,
                                  self.X_valid,
                                  self.y_true,
                                  cmap = plt.cm.Blues)

            plt.title("Confusion Matrix For: " + model_name)
            plt.show()


    def show_classification_report(self):

        for col in self.preds_df.columns:

            clf_report = classification_report(self.y_true, self.preds_df.loc[:,col], output_dict=True)
            clf_report_print = classification_report(self.y_true, self.preds_df.loc[:, col])

            print("\n\n" + col)
            print(clf_report_print)
            sns.heatmap(pd.DataFrame(clf_report).T,
                        annot = True, vmin = 0, vmax = 1,
                        cmap = plt.cm.Blues)

            plt.title("Classification Report for: " + col)
            plt.show()


    def explore_feature_distributions(self):
        pass

    def explore_statistics_for_hardest(self):
        """
        This function checks out the z-scores
        and other important statistics
        for each of the hardest

        :return:
        """
        pass

    def explore_features_for_hardest(self):
        """
        Checks out each feature and color codes the
        'hardest' to categorize - seeing if the harder
        samples have anything in common
        feature-wise.


        Displays feature distributions with sample
        difficulty coded ordinally.

        :return:
        """
        pass
    def show_best_recall(self):
        pass

    def show_best_precision(self):
        pass

    def show_best_f1(self):
        pass

    def show_best_on_hardest_samples(self):
        pass

    def show_confidence_on_hardest_samples(self):
        pass

    def get_best_on_particular_rows(self):
        pass

    def ensemble_analysis(self):
        # Which ensemble gives the best results?

        # Create different combinations of all the preds
        # Add the ensembles to the confusion matrices / classification reports!
        # Voting classifiers
        # Stacking Classifiers
        # Mean and Median Classifiers

        pass

    def show_all_reports(self):

        for col, model in zip(self.preds_df.columns, self.models):

            assert(model[1] == col)  # The column name must equal the model name

            # plt.subplots - Confusion matrix and Classification report
            # Speed

        # Overall Reports:
        # Best Precision
        # Best Recall
        # Best f1 Score.
        # Best Accuracy.

        # Diversity Analysis.


    def do_binary_metrics(self):
        pass

    def get_num_wrong_right(self):
        """

        :return: a df of number right, wrong, and proportions
        """

        num_rightwrong_df = pd.DataFrame()


    def fit_accuracy_scores(self):
        """
        Redundant function now?
        Remove?

        :return:
        """

        self.add_to_metrics_from_ytrue_and_preds_df(
            func=sklearn.metrics.accuracy_score,
            func_name="accuracy_score")


    def get_classification_metrics(self):

        """
        ANALYZE: assumes fit_predicted data already
        and just needs self.preds_df.

        Get classification_metrics for each of the classifiers

        :return:
        """
        # Call helper function to find if this is a multi-class problem
        # or a binary classification problem.

        # Make this configurable
        multiclass_kwargs = {"average":"micro"}

        metric_names = ["accuracy", "recall_score", "precision_score", "f1_score"]

        self.metrics_df = pd.DataFrame(index = metric_names)

        # Need a better way to do this!!!!!!!!!
        # Nested for loop?  Apply?

    def analyze(self):
        pass

    def find_hardest_samples(self):
        """
        ANALYZE:

        These are the samples that were the hardest to
        get correct.

        For each sample, find total "correct" and "wrong"
        Sort these results by the most wrong.

        FOLLOW UP:
        Then do a cluster / correlation / dependency analysis
        in the X field on these samples to find out
        if they have something in common.

        :return:
        """

        trues_df = self.preds_df.copy()

        # Set all to the trues for easy comparison.
        for col in trues_df.columns:
            trues_df[col] = self.y_true

        correct_mask = trues_df == self.preds_df


        self.correct_mask = correct_mask

        n_correct = correct_mask.sum(axis = 1)

        mask_with_margins = correct_mask.insert(0, "n_clf_correct", n_correct)

        # TODO: This doesn't do what I want.  It is still set to "correct_mask"
        self.correct_mask_with_margins_ = mask_with_margins

        n_correct = n_correct.sort_values()
        self.hardest_samples_ = n_correct

        print("\nSorted Hardest Samples: retrievable with the .hardest_samples_ attribute")
        print("Key is row index of sample, Value is the number of correct from all predictors")
        print(n_correct)

        self.n_freq_correct = n_correct.value_counts().sort_values()

        print("\nNumber of correct: retrievable with the .n_freq_correct attribute_")
        print("Index is the number of correct predictions, value is how many samples had that number of correct")
        print(self.n_freq_correct)

        print("\nFull Mask: retrievable with the .correct_mask attribute")
        print(mask_with_margins)

        print(self.correct_mask)

    def cluster_wrong_answers(self):
        """
        Find out if wrong answers have anything in common.

        :return:
        """
        pass

    def find_most_variance(self):
        """
        This function finds the samples that had
        the most variance across them.

        Highest std / variance.

        What does this mean in terms of Classification?
        Most different guesses.


        :return:
        """
        pass

    def analyze_ensemble(self):
        pass

    def add_to_ensembled_preds_df_with_ensemble_func(self):
        """
        Generalize the below to deal with any aggregation function.

        :return:
        """

    def add_metric_to_metric_df(self,
                                func,
                                func_name):
        """
        I've been concatenating but this leaves double rows
        of the same metric.

        Solve this problem by calling this function when adding
        another metric to a DF that already has other metrics
        OR is blank.

        :return:
        """
        new_preds = func(axis=1)

        # TODO: Check for Rounding Bias
        new_preds_df = pd.DataFrame(new_preds, columns=[func_name]).round(decimals = 0).astype(int)

        # ADD: IF THERE IS ALREADY A MEAN ROW, DROP IT.
        # Code here

        # Add Here
        self.ensembled_preds_df = pd.concat([self.ensembled_preds_df, new_preds_df], axis = 1)


    def fit_mean_ensemble(self):
        self.add_metric_to_metric_df(self.preds_df.mean,
                                     "mean_ensemble")


    def fit_median_ensemble(self):
        self.add_metric_to_metric_df(self.preds_df.median,
                                     "median_ensemble")

    def fit_mode_ensemble(self):

        # This doesn't work.
        # Gives ValueError: Cannot convert non-finite values (NA or inf) to integer

        #self.add_metric_to_metric_df(self.preds_df.mode,
        #                             "mode_ensemble")
        pass

    def fit_all_stats_ensembles(self):

        self.fit_mean_ensemble()
        self.fit_median_ensemble()


    def fit_best_ensemble(self):
        """

        :return:
        """
        pass

    def fit_null_test(self):
        """
        Create random predictions in a certain range
        and see how that compares with your other
        models.

        :return:
        """
        pass

    def fit_random_seed_variance(self):
        """
        How much variance is there in just changing the random seed
        :return:
        """
        pass

    def correlated_predictions(self):
        """
        Get diverse predictors by finding uncorrelated predictions.

        :return:
        """
        pass

    def ensemble_from_pred_columns(self):
        pass

    def combinatorial_ensemble(self):

        self.ensemble_comb_preds = pd.DataFrame(index = self.preds_df.index)

        cols = self.preds_df.columns
        length_cols = len(cols)

        for num_columns in range(2, length_cols):
            column_combinations = combinations(cols, num_columns)

            for the_cols in column_combinations:
                # Put ensembler loop in here.

                pass


    def bootstrap(self):
        pass

