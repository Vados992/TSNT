"""Auditable edge ingestion from an explicitly supplied CSV file."""

import csv
from datetime import datetime
from io import StringIO
from pathlib import Path

from tsnt.data.provenance import ProvenanceRecord, sha256_bytes
from tsnt.domain.enums import EvidenceClass, Layer
from tsnt.domain.models import EdgeRecord
from tsnt.ingestion.base import DataAccessError, IngestionAdapter, IngestionBatch


class CSVEdgeAdapter(IngestionAdapter):
    def __init__(self, path: Path, provenance: ProvenanceRecord) -> None:
        self.path = path
        self.provenance = provenance

    def fetch(self, valid_from: datetime, valid_to: datetime) -> IngestionBatch:
        payload = self.path.read_bytes()
        if sha256_bytes(payload) != self.provenance.checksum_sha256:
            raise DataAccessError("CSV content does not match its provenance checksum")
        edges: list[EdgeRecord] = []
        with StringIO(payload.decode("utf-8")) as handle:
            for row in csv.DictReader(handle):
                edge = EdgeRecord(
                    edge_id=row["edge_id"],
                    source=row["source"],
                    target=row["target"],
                    layer=Layer(row["layer"]),
                    commodity=row["commodity"],
                    capacity=float(row["capacity"]),
                    cost_per_unit=float(row.get("cost_per_unit", 0)),
                    transit_time_days=float(row.get("transit_time_days", 0)),
                    canonical_flow_id=row.get("canonical_flow_id") or None,
                    unit=row.get("unit") or "unit/day",
                    evidence_class=EvidenceClass(row.get("evidence_class") or "synthetic"),
                    valid_from=datetime.fromisoformat(row["valid_from"]),
                    valid_to=(
                        datetime.fromisoformat(row["valid_to"])
                        if row.get("valid_to")
                        else None
                    ),
                    transaction_time=datetime.fromisoformat(row["transaction_time"]),
                )
                active = edge.valid_from < valid_to and (
                    edge.valid_to is None or edge.valid_to > valid_from
                )
                if active:
                    edges.append(edge)
        return IngestionBatch((), tuple(edges), self.provenance)
