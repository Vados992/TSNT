"""Seeded Monte Carlo execution with quantiles and exceedance probabilities."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass

import numpy as np
from numpy.random import Generator


@dataclass(frozen=True, slots=True)
class DistributionSummary:
    mean: float
    standard_deviation: float
    minimum: float
    p10: float
    p50: float
    p90: float
    maximum: float
    exceedance_probability: float | None


@dataclass(frozen=True, slots=True)
class MonteCarloResult:
    runs: int
    seed: int
    outputs: dict[str, DistributionSummary]


Sampler = Callable[[Generator], Mapping[str, float]]
Model = Callable[[Mapping[str, float]], float | Mapping[str, float]]


def run_monte_carlo(
    sampler: Sampler,
    model: Model,
    runs: int,
    seed: int = 0,
    exceedance_thresholds: Mapping[str, float] | None = None,
) -> MonteCarloResult:
    if runs < 1:
        raise ValueError("runs must be positive")
    rng = np.random.default_rng(seed)
    columns: dict[str, list[float]] = {}
    expected_keys: set[str] | None = None
    for _ in range(runs):
        raw = model(sampler(rng))
        output = {"value": float(raw)} if isinstance(raw, (int, float)) else raw
        keys = set(output)
        if expected_keys is None:
            expected_keys = keys
        elif keys != expected_keys:
            raise ValueError("model output keys changed between Monte Carlo runs")
        for name, value in output.items():
            number = float(value)
            if not np.isfinite(number):
                raise ValueError(f"non-finite Monte Carlo output: {name}")
            columns.setdefault(name, []).append(number)

    thresholds = exceedance_thresholds or {}
    summaries: dict[str, DistributionSummary] = {}
    for name, values in columns.items():
        array = np.asarray(values)
        quantiles = np.quantile(array, [0.1, 0.5, 0.9])
        threshold = thresholds.get(name)
        probability = None if threshold is None else float(np.mean(array > threshold))
        summaries[name] = DistributionSummary(
            mean=float(np.mean(array)),
            standard_deviation=float(np.std(array, ddof=1)) if runs > 1 else 0.0,
            minimum=float(np.min(array)),
            p10=float(quantiles[0]),
            p50=float(quantiles[1]),
            p90=float(quantiles[2]),
            maximum=float(np.max(array)),
            exceedance_probability=probability,
        )
    return MonteCarloResult(runs=runs, seed=seed, outputs=summaries)
