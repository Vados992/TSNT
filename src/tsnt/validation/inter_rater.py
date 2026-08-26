"""Inter-rater reliability for continuous scores and rankings."""

import numpy as np
from scipy.stats import rankdata


def icc_2k(ratings: np.ndarray) -> float:
    """Two-way random-effects, absolute-agreement ICC for mean ratings."""
    data = np.asarray(ratings, dtype=float)
    if data.ndim != 2 or min(data.shape) < 2 or not np.all(np.isfinite(data)):
        raise ValueError("ratings must be a finite targets-by-raters matrix")
    targets, raters = data.shape
    grand = float(np.mean(data))
    row_means = np.mean(data, axis=1)
    column_means = np.mean(data, axis=0)
    ss_rows = raters * float(np.sum(np.square(row_means - grand)))
    ss_columns = targets * float(np.sum(np.square(column_means - grand)))
    residual = data - row_means[:, None] - column_means[None, :] + grand
    ss_error = float(np.sum(np.square(residual)))
    ms_rows = ss_rows / (targets - 1)
    ms_columns = ss_columns / (raters - 1)
    ms_error = ss_error / ((targets - 1) * (raters - 1))
    denominator = ms_rows + (ms_columns - ms_error) / targets
    if denominator == 0:
        raise ValueError("ICC is undefined for constant ratings")
    return float((ms_rows - ms_error) / denominator)


def kendalls_w(scores: np.ndarray) -> float:
    """Kendall coefficient of concordance with tie correction."""
    data = np.asarray(scores, dtype=float)
    if data.ndim != 2 or min(data.shape) < 2 or not np.all(np.isfinite(data)):
        raise ValueError("scores must be a finite items-by-raters matrix")
    items, raters = data.shape
    ranks = np.column_stack([rankdata(data[:, index]) for index in range(raters)])
    rank_sums = np.sum(ranks, axis=1)
    dispersion = float(np.sum(np.square(rank_sums - np.mean(rank_sums))))
    tie_total = 0.0
    for index in range(raters):
        _, counts = np.unique(data[:, index], return_counts=True)
        tie_total += float(np.sum(counts**3 - counts))
    denominator = raters**2 * (items**3 - items) - raters * tie_total
    if denominator == 0:
        raise ValueError("Kendall W is undefined when every rater assigns only ties")
    return float(12 * dispersion / denominator)
