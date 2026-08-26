"""Controls against correlated indicators and duplicated physical flows."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, slots=True)
class DoubleCountReport:
    duplicate_flow_ids: tuple[str, ...]
    high_correlation_pairs: tuple[tuple[str, str, float], ...]
    variance_inflation_factors: dict[str, float]
    passed: bool


def _vif(values: np.ndarray, index: int) -> float:
    target = values[:, index]
    others = np.delete(values, index, axis=1)
    if others.shape[1] == 0:
        return 1.0
    design = np.column_stack([np.ones(values.shape[0]), others])
    fitted = design @ np.linalg.lstsq(design, target, rcond=None)[0]
    total = float(np.sum(np.square(target - np.mean(target))))
    if total == 0:
        return float("inf")
    residual = float(np.sum(np.square(target - fitted)))
    r_squared = max(0.0, min(1.0, 1.0 - residual / total))
    return float("inf") if r_squared >= 1 - 1e-12 else 1.0 / (1.0 - r_squared)


def audit_double_counting(
    indicator_names: list[str],
    observations: np.ndarray,
    canonical_flow_ids: list[str] | None = None,
    correlation_limit: float = 0.9,
    vif_limit: float = 10.0,
) -> DoubleCountReport:
    data = np.asarray(observations, dtype=float)
    if data.ndim != 2 or data.shape[1] != len(indicator_names) or data.shape[0] < 3:
        raise ValueError("observations must be rows-by-indicators with at least three rows")
    if len(set(indicator_names)) != len(indicator_names) or not np.all(np.isfinite(data)):
        raise ValueError("indicator names must be unique and observations finite")
    if not 0 < correlation_limit <= 1 or vif_limit <= 1:
        raise ValueError("invalid correlation or VIF limit")

    ids = canonical_flow_ids or []
    duplicates = tuple(sorted({flow_id for flow_id in ids if ids.count(flow_id) > 1}))
    correlation = np.corrcoef(data, rowvar=False)
    pairs: list[tuple[str, str, float]] = []
    for left in range(len(indicator_names)):
        for right in range(left + 1, len(indicator_names)):
            value = float(correlation[left, right])
            if np.isfinite(value) and abs(value) >= correlation_limit:
                pairs.append((indicator_names[left], indicator_names[right], value))
    vifs = {name: _vif(data, index) for index, name in enumerate(indicator_names)}
    passed = not duplicates and not pairs and all(value < vif_limit for value in vifs.values())
    return DoubleCountReport(duplicates, tuple(pairs), vifs, passed)
