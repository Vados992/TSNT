"""Pydantic contracts shared by ingestion, models and the API."""

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from tsnt.domain.enums import EvidenceClass, Layer


class FrozenModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class NodeComponents(FrozenModel):
    centrality: float = Field(ge=0, le=10)
    throughput: float = Field(ge=0, le=10)
    control: float = Field(ge=0, le=10)
    cascade: float = Field(ge=0, le=10)
    substitutability: float = Field(ge=0, le=10)


class BitemporalRecord(FrozenModel):
    valid_from: datetime
    valid_to: datetime | None = None
    transaction_time: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def validate_interval(self) -> "BitemporalRecord":
        if self.valid_to is not None and self.valid_to <= self.valid_from:
            raise ValueError("valid_to must be later than valid_from")
        return self


class NodeRecord(BitemporalRecord):
    node_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    layer: Layer
    jurisdiction: str | None = None
    components: NodeComponents | None = None
    evidence_class: EvidenceClass = EvidenceClass.SYNTHETIC


class EdgeRecord(BitemporalRecord):
    edge_id: str = Field(min_length=1)
    source: str = Field(min_length=1)
    target: str = Field(min_length=1)
    layer: Layer
    commodity: str = Field(min_length=1)
    capacity: float = Field(ge=0)
    cost_per_unit: float = Field(default=0, ge=0)
    transit_time_days: float = Field(default=0, ge=0)
    canonical_flow_id: str | None = None
    unit: str = Field(default="unit/day", min_length=1)
    evidence_class: EvidenceClass = EvidenceClass.SYNTHETIC

    @model_validator(mode="after")
    def distinct_endpoints(self) -> "EdgeRecord":
        if self.source == self.target:
            raise ValueError("self-loop flow edges are not supported")
        return self


class CapacityShock(FrozenModel):
    target_type: Literal["edge", "node", "layer"]
    target_id: str = Field(min_length=1)
    capacity_factor: float = Field(ge=0, le=1)
    starts_at: datetime
    ends_at: datetime | None = None
    rationale: str = Field(min_length=1)

    def active_at(self, moment: datetime) -> bool:
        return self.starts_at <= moment and (self.ends_at is None or moment < self.ends_at)


class ScenarioContract(FrozenModel):
    scenario_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    as_of: datetime
    analysis_cutoff: datetime
    horizon_days: int = Field(default=30, ge=1, le=3650)
    random_seed: int = 0
    shocks: tuple[CapacityShock, ...] = ()

    @model_validator(mode="after")
    def cutoff_not_after_run_time(self) -> "ScenarioContract":
        if self.analysis_cutoff > self.as_of:
            raise ValueError("analysis_cutoff cannot be later than as_of")
        return self


class OutputVector(FrozenModel):
    snii: float | None = None
    hazard: float | None = None
    delta_flow: float
    delta_cost: float
    delta_time: float
    delta_output: float
    cascade_depth: int
    time_to_recovery: float | None = None
    control_vector: dict[str, float] = Field(default_factory=dict)
    confidence: float = Field(ge=0, le=1)
