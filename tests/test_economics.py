import numpy as np
import pytest

from tsnt.economics.input_output import leontief_output, supply_constrained_allocation


def test_leontief_solution_satisfies_accounting_identity():
    coefficients = np.array([[0.2, 0.1], [0.1, 0.2]])
    demand = np.array([8.0, 4.0])
    result = leontief_output(coefficients, demand)
    assert np.allclose((np.eye(2) - coefficients) @ result.gross_output, demand)
    assert result.spectral_radius < 1


def test_unproductive_leontief_system_is_rejected():
    with pytest.raises(ValueError, match="spectral radius"):
        leontief_output(np.array([[1.0]]), np.array([1.0]))


def test_supply_constraint_limits_delivered_demand():
    result = supply_constrained_allocation(
        np.zeros((2, 2)),
        np.array([10.0, 8.0]),
        np.array([6.0, 5.0]),
    )
    assert np.allclose(result.delivered_final_demand, [6, 5])
    assert np.allclose(result.unmet_final_demand, [4, 3])
