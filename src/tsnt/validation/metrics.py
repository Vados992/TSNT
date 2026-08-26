"""Forecast and probabilistic validation metrics."""

import numpy as np


def _pair(actual: np.ndarray, predicted: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    y = np.asarray(actual, dtype=float)
    p = np.asarray(predicted, dtype=float)
    if y.shape != p.shape or y.size == 0:
        raise ValueError("actual and predicted must have the same non-empty shape")
    if not np.all(np.isfinite(y)) or not np.all(np.isfinite(p)):
        raise ValueError("metrics require finite values")
    return y, p


def mae(actual: np.ndarray, predicted: np.ndarray) -> float:
    y, p = _pair(actual, predicted)
    return float(np.mean(np.abs(y - p)))


def rmse(actual: np.ndarray, predicted: np.ndarray) -> float:
    y, p = _pair(actual, predicted)
    return float(np.sqrt(np.mean(np.square(y - p))))


def smape(actual: np.ndarray, predicted: np.ndarray) -> float:
    y, p = _pair(actual, predicted)
    denominator = np.abs(y) + np.abs(p)
    terms = np.divide(
        2 * np.abs(p - y),
        denominator,
        out=np.zeros_like(denominator),
        where=denominator != 0,
    )
    return float(np.mean(terms))


def pinball_loss(actual: np.ndarray, quantile_prediction: np.ndarray, quantile: float) -> float:
    if not 0 < quantile < 1:
        raise ValueError("quantile must be between 0 and 1")
    y, p = _pair(actual, quantile_prediction)
    error = y - p
    return float(np.mean(np.maximum(quantile * error, (quantile - 1) * error)))


def interval_coverage(actual: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> float:
    y, low = _pair(actual, lower)
    _, high = _pair(actual, upper)
    if np.any(low > high):
        raise ValueError("lower interval cannot exceed upper interval")
    return float(np.mean((y >= low) & (y <= high)))


def brier_score(outcomes: np.ndarray, probabilities: np.ndarray) -> float:
    y, p = _pair(outcomes, probabilities)
    if np.any((y != 0) & (y != 1)) or np.any((p < 0) | (p > 1)):
        raise ValueError("Brier score requires binary outcomes and probabilities in [0,1]")
    return float(np.mean(np.square(p - y)))
