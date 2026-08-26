import numpy as np

from tsnt.cascade.engine import simulate_cascade


def test_chain_cascade_reports_depth_and_affected_nodes():
    influence = np.array(
        [
            [0.0, 0.0, 0.0],
            [0.8, 0.0, 0.0],
            [0.0, 0.8, 0.0],
        ]
    )
    result = simulate_cascade(influence, np.array([1.0, 0.0, 0.0]))
    assert result.converged
    assert result.affected_indices == (0, 1, 2)
    assert result.cascade_depth == 2
