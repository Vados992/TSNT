"""Piecewise-linear service recovery metrics."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, slots=True)
class RecoveryResult:
    time_to_recovery: float | None
    cumulative_service_loss: float
    threshold: float
    sustained_window: float


def _minimum_on_interval(
    times: np.ndarray,
    service: np.ndarray,
    start: float,
    end: float,
) -> float:
    interior = times[(times > start) & (times < end)]
    probes = np.concatenate(([start], interior, [end]))
    return float(np.min(np.interp(probes, times, service)))


def analyse_recovery(
    times: np.ndarray,
    service_levels: np.ndarray,
    threshold: float = 0.9,
    sustained_window: float = 0.0,
) -> RecoveryResult:
    """Calculate deficit area and first sustained crossing of a service threshold."""
    x = np.asarray(times, dtype=float)
    y = np.asarray(service_levels, dtype=float)
    if x.ndim != 1 or y.shape != x.shape or x.size < 2:
        raise ValueError("times and service_levels must be equal one-dimensional arrays")
    if np.any(np.diff(x) <= 0) or np.any(y < 0) or np.any(y > 1):
        raise ValueError("times must increase and service levels must be within [0,1]")
    if not 0 <= threshold <= 1 or sustained_window < 0:
        raise ValueError("invalid recovery threshold or sustained window")

    candidates: list[float] = []
    for index in range(x.size):
        if y[index] >= threshold:
            candidates.append(float(x[index]))
        if index and y[index - 1] < threshold <= y[index]:
            fraction = (threshold - y[index - 1]) / (y[index] - y[index - 1])
            candidates.append(float(x[index - 1] + fraction * (x[index] - x[index - 1])))

    recovery: float | None = None
    for candidate in sorted(set(candidates)):
        end = candidate + sustained_window
        if end <= x[-1] and _minimum_on_interval(x, y, candidate, end) >= threshold - 1e-12:
            recovery = candidate
            break

    loss = float(np.trapezoid(1.0 - y, x))
    return RecoveryResult(recovery, loss, threshold, sustained_window)
