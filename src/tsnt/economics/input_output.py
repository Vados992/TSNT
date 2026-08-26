"""Leontief accounting and a transparent supply-constrained linear program."""

from dataclasses import dataclass

import numpy as np
from scipy.optimize import linprog


@dataclass(frozen=True, slots=True)
class LeontiefResult:
    gross_output: np.ndarray
    spectral_radius: float
    condition_number: float


@dataclass(frozen=True, slots=True)
class IOAllocation:
    gross_output: np.ndarray
    delivered_final_demand: np.ndarray
    unmet_final_demand: np.ndarray
    objective_value: float


def _validate_system(coefficients: np.ndarray, vector: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    matrix = np.asarray(coefficients, dtype=float)
    values = np.asarray(vector, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("coefficients must be a square matrix")
    if values.shape != (matrix.shape[0],):
        raise ValueError("vector length must equal the matrix dimension")
    if np.any(matrix < 0) or np.any(values < 0):
        raise ValueError("coefficients and vectors must be non-negative")
    return matrix, values


def leontief_output(
    coefficients: np.ndarray,
    final_demand: np.ndarray,
    condition_limit: float = 1e12,
) -> LeontiefResult:
    """Solve x=(I-A)^-1 f after stability and conditioning checks."""
    matrix, demand = _validate_system(coefficients, final_demand)
    radius = float(max(abs(np.linalg.eigvals(matrix)), default=0.0))
    system = np.eye(matrix.shape[0]) - matrix
    condition = float(np.linalg.cond(system))
    if radius >= 1:
        raise ValueError("Leontief system is not productive: spectral radius must be below 1")
    if not np.isfinite(condition) or condition > condition_limit:
        raise ValueError("Leontief system is numerically ill-conditioned")
    output = np.linalg.solve(system, demand)
    return LeontiefResult(output, radius, condition)


def supply_constrained_allocation(
    coefficients: np.ndarray,
    final_demand: np.ndarray,
    capacity: np.ndarray,
    net_imports: np.ndarray | None = None,
    priorities: np.ndarray | None = None,
) -> IOAllocation:
    """Allocate scarce output using Ax+y <= x+imports and capacity bounds."""
    matrix, demand = _validate_system(coefficients, final_demand)
    cap = np.asarray(capacity, dtype=float)
    imports = np.zeros_like(demand) if net_imports is None else np.asarray(net_imports, dtype=float)
    weight = np.ones_like(demand) if priorities is None else np.asarray(priorities, dtype=float)
    expected = demand.shape
    if cap.shape != expected or imports.shape != expected or weight.shape != expected:
        raise ValueError("capacity, imports and priorities must match final_demand")
    if np.any(cap < 0) or np.any(imports < 0) or np.any(weight < 0):
        raise ValueError("capacity, imports and priorities must be non-negative")

    size = demand.size
    objective = np.concatenate([np.zeros(size), -weight])
    constraints = np.hstack([matrix - np.eye(size), np.eye(size)])
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=imports,
        bounds=[(0.0, float(value)) for value in cap]
        + [(0.0, float(value)) for value in demand],
        method="highs",
    )
    if not result.success:
        raise RuntimeError(f"supply-constrained IO optimization failed: {result.message}")
    output = np.asarray(result.x[:size])
    delivered = np.asarray(result.x[size:])
    return IOAllocation(
        gross_output=output,
        delivered_final_demand=delivered,
        unmet_final_demand=demand - delivered,
        objective_value=float(-result.fun),
    )
