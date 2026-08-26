from datetime import UTC, datetime, timedelta

import numpy as np
import pytest

from tsnt.validation.backtest import BacktestRecord, run_backtest
from tsnt.validation.inter_rater import icc_2k, kendalls_w
from tsnt.validation.metrics import brier_score, interval_coverage, mae, rmse


def test_metrics_have_known_values():
    actual = np.array([0.0, 1.0, 2.0])
    predicted = np.array([0.0, 2.0, 1.0])
    assert mae(actual, predicted) == pytest.approx(2 / 3)
    assert rmse(actual, predicted) == pytest.approx((2 / 3) ** 0.5)
    assert interval_coverage(actual, actual - 0.1, actual + 0.1) == 1
    assert brier_score(np.array([0, 1]), np.array([0.25, 0.75])) == 0.0625


def test_inter_rater_agreement_is_one_for_identical_raters():
    ratings = np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3]], dtype=float)
    assert icc_2k(ratings) == pytest.approx(1)
    assert kendalls_w(ratings) == pytest.approx(1)


def test_backtest_rejects_future_information():
    cutoff = datetime(2024, 1, 1, tzinfo=UTC)
    record = BacktestRecord(
        "event",
        predicted=1,
        actual=1,
        lower=0,
        upper=2,
        transaction_time=cutoff + timedelta(seconds=1),
    )
    with pytest.raises(ValueError, match="temporal leakage"):
        run_backtest([record], cutoff)
