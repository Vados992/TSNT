import numpy as np
import pytest

from tsnt.recovery.model import analyse_recovery


def test_piecewise_recovery_interpolates_threshold():
    result = analyse_recovery(
        np.array([0.0, 1.0, 2.0, 3.0]),
        np.array([0.2, 0.6, 0.9, 1.0]),
        threshold=0.8,
        sustained_window=1.0,
    )
    assert result.time_to_recovery == pytest.approx(5 / 3)
    assert result.cumulative_service_loss > 0
