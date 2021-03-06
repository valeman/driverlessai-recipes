"""Largest error for regression problems. Highly sensitive to outliers."""
import typing
import numpy as np
from h2oaicore.metrics import CustomScorer


class MyLargestErrorScorer(CustomScorer):
    _description = "My Largest Error Scorer for Regression."
    _regression = True
    _maximize = False
    _perfect_score = 0
    _display_name = "LargestError"

    def score(self,
              actual: np.array,
              predicted: np.array,
              sample_weight: typing.Optional[np.array] = None,
              labels: typing.Optional[np.array] = None,
              **kwargs) -> float:
        absdiff = np.abs(actual - predicted)
        if sample_weight is not None:
            return absdiff[sample_weight != 0].max()
        return absdiff.max()
