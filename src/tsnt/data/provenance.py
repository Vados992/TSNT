"""Machine-readable source and transformation lineage."""

import hashlib
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from tsnt.domain.enums import EvidenceClass


class LineageStep(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    operation: str = Field(min_length=1)
    code_version: str = Field(min_length=1)
    executed_at: datetime
    parameters: dict[str, str | int | float | bool] = Field(default_factory=dict)


class ProvenanceRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    provenance_id: str = Field(min_length=1)
    source_name: str = Field(min_length=1)
    source_uri: str = Field(min_length=1)
    retrieved_at: datetime
    effective_time: datetime
    evidence_class: EvidenceClass
    licence_id: str = Field(min_length=1)
    checksum_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    analyst_id: str | None = None
    lineage: tuple[LineageStep, ...] = ()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()
