from datetime import UTC, datetime

import pytest

from tsnt.domain.enums import EvidenceClass, Layer
from tsnt.domain.models import EdgeRecord


@pytest.fixture
def edge_factory():
    now = datetime(2026, 1, 1, tzinfo=UTC)

    def build(edge_id, source, target, capacity, cost=0.0, transit=0.0):
        return EdgeRecord(
            edge_id=edge_id,
            source=source,
            target=target,
            layer=Layer.TRADE,
            commodity="synthetic",
            capacity=capacity,
            cost_per_unit=cost,
            transit_time_days=transit,
            valid_from=now,
            transaction_time=now,
            evidence_class=EvidenceClass.SYNTHETIC,
        )

    return build
