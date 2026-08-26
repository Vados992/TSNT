"""Unit conversion and hard acceptance gates for analytical inputs."""

from collections import Counter
from dataclasses import dataclass
from math import isfinite

from tsnt.domain.models import EdgeRecord


@dataclass(frozen=True, slots=True)
class QualityIssue:
    code: str
    message: str
    record_id: str | None = None
    severity: str = "error"


@dataclass(frozen=True, slots=True)
class QualityReport:
    issues: tuple[QualityIssue, ...]
    checked_records: int

    @property
    def passed(self) -> bool:
        return not any(issue.severity == "error" for issue in self.issues)


class UnitRegistry:
    """Small explicit registry; integrations should add reviewed conversions only."""

    _units: dict[str, tuple[str, float]] = {
        "unit/day": ("generic_flow", 1.0),
        "tonne/day": ("mass_flow", 1.0),
        "kt/day": ("mass_flow", 1_000.0),
        "bbl/day": ("oil_flow", 1.0),
        "kbbl/day": ("oil_flow", 1_000.0),
        "m3/day": ("volume_flow", 1.0),
        "mcm/day": ("volume_flow", 1_000_000.0),
        "mw": ("power", 1.0),
        "gw": ("power", 1_000.0),
        "usd/day": ("value_flow", 1.0),
    }

    def convert(self, value: float, source: str, target: str) -> float:
        if source not in self._units or target not in self._units:
            raise ValueError("unregistered unit")
        source_dimension, source_factor = self._units[source]
        target_dimension, target_factor = self._units[target]
        if source_dimension != target_dimension:
            raise ValueError("cannot convert between different dimensions")
        return value * source_factor / target_factor

    def is_registered(self, unit: str) -> bool:
        return unit in self._units


class QualityGate:
    def __init__(self, units: UnitRegistry | None = None) -> None:
        self.units = units or UnitRegistry()

    def validate_edges(self, edges: list[EdgeRecord]) -> QualityReport:
        issues: list[QualityIssue] = []
        edge_counts = Counter(edge.edge_id for edge in edges)
        for edge_id, count in edge_counts.items():
            if count > 1:
                issues.append(QualityIssue("duplicate_edge_id", f"{count} versions in batch", edge_id))
        flow_ids = [edge.canonical_flow_id for edge in edges if edge.canonical_flow_id]
        for flow_id, count in Counter(flow_ids).items():
            if count > 1:
                issues.append(
                    QualityIssue(
                        "duplicate_canonical_flow",
                        "same physical flow appears more than once in the analytical batch",
                        flow_id,
                    )
                )
        for edge in edges:
            if not self.units.is_registered(edge.unit):
                issues.append(QualityIssue("unknown_unit", edge.unit, edge.edge_id))
            if not isfinite(edge.capacity) or not isfinite(edge.cost_per_unit):
                issues.append(QualityIssue("non_finite", "capacity or cost is non-finite", edge.edge_id))
            if edge.transaction_time < edge.valid_from:
                issues.append(
                    QualityIssue(
                        "publication_before_effective_time",
                        "verify source timing; this may be legitimate advance publication",
                        edge.edge_id,
                        "warning",
                    )
                )
        return QualityReport(tuple(issues), len(edges))

    def require_edges(self, edges: list[EdgeRecord]) -> None:
        report = self.validate_edges(edges)
        if not report.passed:
            details = "; ".join(f"{item.code}:{item.record_id}" for item in report.issues)
            raise ValueError(f"edge quality gate failed: {details}")
