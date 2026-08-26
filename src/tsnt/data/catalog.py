"""In-memory catalog contract; production deployments can back it with SQL."""

from dataclasses import dataclass, field
from datetime import UTC, datetime

from tsnt.data.provenance import ProvenanceRecord


@dataclass(slots=True)
class DataCatalog:
    records: dict[str, ProvenanceRecord] = field(default_factory=dict)
    last_seen: dict[str, datetime] = field(default_factory=dict)

    def register(self, record: ProvenanceRecord) -> None:
        if record.provenance_id in self.records:
            existing = self.records[record.provenance_id]
            if existing.checksum_sha256 != record.checksum_sha256:
                raise ValueError("provenance_id cannot be reused for different content")
        self.records[record.provenance_id] = record
        self.last_seen[record.source_name] = datetime.now(UTC)

    def require(self, provenance_id: str) -> ProvenanceRecord:
        try:
            return self.records[provenance_id]
        except KeyError as error:
            raise KeyError(f"unknown provenance_id: {provenance_id}") from error
