"""Bounded cascade propagation over an explicitly supplied dependency matrix."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, slots=True)
class CascadeResult:
    final_state: np.ndarray
    affected_indices: tuple[int, ...]
    cascade_depth: int
    converged: bool
    spectral_radius: float
    history: tuple[np.ndarray, ...]


def simulate_cascade(
    influence: np.ndarray,
    initial_shock: np.ndarray,
    threshold: float = 0.5,
    max_steps: int = 100,
    tolerance: float = 1e-9,
) -> CascadeResult:
    """Iterate z(k+1)=clip(s+Bz(k),0,1) until convergence."""
    matrix = np.asarray(influence, dtype=float)
    shock = np.asarray(initial_shock, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("influence must be square")
    if shock.shape != (matrix.shape[0],):
        raise ValueError("initial_shock length must match influence")
    if np.any(matrix < 0) or np.any(shock < 0) or np.any(shock > 1):
        raise ValueError("influence must be non-negative and shocks must be within [0,1]")
    if not 0 <= threshold <= 1 or max_steps < 1 or tolerance <= 0:
        raise ValueError("invalid convergence parameters")

    state = shock.copy()
    history = [state.copy()]
    first_affected = set(np.flatnonzero(state >= threshold).tolist())
    depth = 0
    converged = False
    for step in range(1, max_steps + 1):
        next_state = np.clip(shock + matrix @ state, 0.0, 1.0)
        newly_affected = set(np.flatnonzero(next_state >= threshold).tolist()) - first_affected
        if newly_affected:
            depth = step
            first_affected.update(newly_affected)
        history.append(next_state.copy())
        if np.max(np.abs(next_state - state)) <= tolerance:
            state = next_state
            converged = True
            break
        state = next_state

    radius = float(max(abs(np.linalg.eigvals(matrix)), default=0.0))
    return CascadeResult(
        final_state=state,
        affected_indices=tuple(sorted(first_affected)),
        cascade_depth=depth,
        converged=converged,
        spectral_radius=radius,
        history=tuple(history),
    )
