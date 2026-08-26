from decimal import Decimal

from tsnt.domain.enums import Layer
from tsnt.domain.models import NodeComponents, NodeRecord
from tsnt.scoring.snii import compute_snii, rank_nodes


def test_snii_uses_exact_weights_and_half_up_rounding():
    components = NodeComponents(
        centrality=10,
        throughput=8,
        control=6,
        cascade=4,
        substitutability=2,
    )
    score = compute_snii(components)
    assert score.exact == Decimal("6.7")
    assert score.published == Decimal("6.70")


def test_rank_nodes_uses_exact_score_before_published_rounding():
    from datetime import UTC, datetime

    now = datetime(2026, 1, 1, tzinfo=UTC)
    high = NodeRecord(
        node_id="high",
        name="High",
        layer=Layer.TRADE,
        components=NodeComponents(
            centrality=5.04,
            throughput=5,
            control=5,
            cascade=5,
            substitutability=5,
        ),
        valid_from=now,
        transaction_time=now,
    )
    low = high.model_copy(
        update={
            "node_id": "low",
            "name": "Low",
            "components": high.components.model_copy(update={"centrality": 5.0}),
        }
    )
    assert [node.node_id for node, _ in rank_nodes([low, high])] == ["high", "low"]
