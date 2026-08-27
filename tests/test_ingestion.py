from datetime import UTC, datetime

import pytest

from tsnt.data.provenance import ProvenanceRecord, sha256_bytes
from tsnt.domain.enums import EvidenceClass
from tsnt.ingestion.base import DataAccessError
from tsnt.ingestion.csv_adapter import CSVEdgeAdapter


def _provenance(checksum, now):
    return ProvenanceRecord(
        provenance_id="fixture",
        source_name="test",
        source_uri="file://fixture",
        retrieved_at=now,
        effective_time=now,
        evidence_class=EvidenceClass.SYNTHETIC,
        licence_id="test-only",
        checksum_sha256=checksum,
    )


def test_csv_adapter_verifies_checksum_and_parses_window(tmp_path):
    now = datetime(2026, 1, 1, tzinfo=UTC)
    content = (
        "edge_id,source,target,layer,commodity,capacity,valid_from,"
        "transaction_time\n"
        "e,s,t,trade,synthetic,3,2026-01-01T00:00:00+00:00,"
        "2026-01-01T00:00:00+00:00\n"
    )
    path = tmp_path / "edges.csv"
    path.write_text(content, encoding="utf-8")
    adapter = CSVEdgeAdapter(path, _provenance(sha256_bytes(content.encode()), now))
    batch = adapter.fetch(now, datetime(2026, 2, 1, tzinfo=UTC))
    assert len(batch.edges) == 1
    assert batch.edges[0].capacity == 3


def test_csv_adapter_rejects_content_drift(tmp_path):
    now = datetime(2026, 1, 1, tzinfo=UTC)
    path = tmp_path / "edges.csv"
    path.write_text("changed", encoding="utf-8")
    adapter = CSVEdgeAdapter(path, _provenance("0" * 64, now))
    with pytest.raises(DataAccessError, match="checksum"):
        adapter.fetch(now, now)
