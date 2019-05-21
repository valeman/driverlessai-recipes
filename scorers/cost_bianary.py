import typing
import numpy as np
from h2oaicore.metrics import CustomScorer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix

class cost_bianary(CustomScorer):
    _description = " Calculates cost in bianary classification: `$1*FP + $2*FN`"
    _binary = True
    _multiclass = False
    _maximize = False
    _perfect_score = 0
    _display_name = "Cost"

    # The cost of false positives and negatives will vary by data set, we use the rules from the below as an example
    # https://www.kaggle.com/uciml/aps-failure-at-scania-trucks-data-set
    _fp_cost = 10
    _fn_cost = 500

    def score(self,
              actual: np.array,
              predicted: np.array,
              sample_weight: typing.Optional[np.array] = None,
              labels: typing.Optional[np.array] = None) -> float:

        # label actuals as 1 or 0
        lb = LabelEncoder()
        labels = lb.fit_transform(labels)
        actual = lb.transform(actual)

        # label predictions as 1 or 0
        predicted = predicted >= 0.5  # probability -> label

        cm = confusion_matrix(actual, predicted, sample_weight=sample_weight, labels=labels)
        tn, fp, fn, tp = cm.ravel()

        return (fp * self.__class__._fp_cost) + (fn * self.__class__._fn_cost)

