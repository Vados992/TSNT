from datetime import UTC, datetime, timedelta

from tsnt.domain.enums import Layer
from tsnt.domain.models import EdgeRecord, NodeRecord
from tsnt.graph.temporal import TemporalMultiLayerGraph


def test_snapshot_excludes_information_published_after_cutoff():
    event_time = datetime(2021, 3, 23, tzinfo=UTC)
    cutoff = event_time
    nodes = [
        NodeRecord(
            node_id=value,
            name=value,
            layer=Layer.MARITIME,
            valid_from=event_time - timedelta(days=1),
            transaction_time=event_time - timedelta(days=1),
        )
        for value in ("a", "b")
    ]
    late_edge = EdgeRecord(
        edge_id="late",
        source="a",
        target="b",
        layer=Layer.MARITIME,
        commodity="synthetic",
        capacity=10,
        valid_from=event_time - timedelta(days=1),
        transaction_time=event_time + timedelta(days=1),
    )
    graph = TemporalMultiLayerGraph(nodes, [late_edge]).snapshot(event_time, cutoff)
    assert graph.number_of_nodes() == 2
    assert graph.number_of_edges() == 0
