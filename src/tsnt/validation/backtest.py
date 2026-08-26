"""Historical backtesting with an explicit information-cutoff firewall."""

from dataclasses import dataclass
from datetime import datetime

import numpy as np

from tsnt.validation.metrics import interval_coverage, mae, rmse, smape


@dataclass(frozen=True, slots=True)
class BacktestRecord:
    event_id: str
    predicted: float
    actual: float
    lower: float
    upper: float
    transaction_time: datetime


@dataclass(frozen=True, slots=True)
class BacktestSummary:
    observations: int
    mae: float
    rmse: float
    smape: float
    interval_coverage: float
    baseline_mae: float | None
    skill_vs_baseline: float | None


def run_backtest(
    records: list[BacktestRecord],
    analysis_cutoff: datetime,
    baseline_predictions: np.ndarray | None = None,
) -> BacktestSummary:
    if not records:
        raise ValueError("backtest requires at least one record")
    leaked = [record.event_id for record in records if record.transaction_time > analysis_cutoff]
    if leaked:
        raise ValueError(f"temporal leakage after cutoff in events: {', '.join(leaked)}")
    actual = np.array([record.actual for record in records], dtype=float)
    predicted = np.array([record.predicted for record in records], dtype=float)
    lower = np.array([record.lower for record in records], dtype=float)
    upper = np.array([record.upper for record in records], dtype=float)

    base_mae: float | None = None
    skill: float | None = None
    if baseline_predictions is not None:
        baseline = np.asarray(baseline_predictions, dtype=float)
        if baseline.shape != actual.shape:
            raise ValueError("baseline_predictions must match records")
        base_mae = mae(actual, baseline)
        skill = None if base_mae == 0 else 1.0 - mae(actual, predicted) / base_mae

    return BacktestSummary(
        observations=len(records),
        mae=mae(actual, predicted),
        rmse=rmse(actual, predicted),
        smape=smape(actual, predicted),
        interval_coverage=interval_coverage(actual, lower, upper),
        baseline_mae=base_mae,
        skill_vs_baseline=skill,
    )
