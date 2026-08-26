"""Bitemporal graph snapshots that prevent historical look-ahead."""

from collections.abc import Iterable
from datetime import datetime

import networkx as nx

from tsnt.domain.models import CapacityShock, EdgeRecord, NodeRecord


class TemporalMultiLayerGraph:
    """Append-only records projected into valid-time/transaction-time snapshots."""

    def __init__(
        self,
        nodes: Iterable[NodeRecord] = (),
        edges: Iterable[EdgeRecord] = (),
    ) -> None:
        self._nodes = list(nodes)
        self._edges = list(edges)

    def add_node(self, node: NodeRecord) -> None:
        self._nodes.append(node)

    def add_edge(self, edge: EdgeRecord) -> None:
        self._edges.append(edge)

    @staticmethod
    def _visible(record: NodeRecord | EdgeRecord, as_of: datetime, cutoff: datetime) -> bool:
        valid = record.valid_from <= as_of and (
            record.valid_to is None or as_of < record.valid_to
        )
        known = record.transaction_time <= cutoff
        return valid and known

    def active_nodes(self, as_of: datetime, analysis_cutoff: datetime) -> list[NodeRecord]:
        return [
            node
            for node in self._nodes
            if self._visible(node, as_of, analysis_cutoff)
        ]

    def active_edges(self, as_of: datetime, analysis_cutoff: datetime) -> list[EdgeRecord]:
        return [
            edge
            for edge in self._edges
            if self._visible(edge, as_of, analysis_cutoff)
        ]

    def snapshot(self, as_of: datetime, analysis_cutoff: datetime) -> nx.MultiDiGraph:
        if analysis_cutoff > as_of:
            raise ValueError("analysis_cutoff cannot be later than as_of")
        graph = nx.MultiDiGraph(as_of=as_of.isoformat(), analysis_cutoff=analysis_cutoff.isoformat())
        active_nodes = self.active_nodes(as_of, analysis_cutoff)
        for node in active_nodes:
            graph.add_node(node.node_id, record=node, layer=node.layer.value)
        known_nodes = set(graph.nodes)
        for edge in self.active_edges(as_of, analysis_cutoff):
            missing = {edge.source, edge.target} - known_nodes
            if missing:
                missing_text = ", ".join(sorted(missing))
                raise ValueError(f"active edge {edge.edge_id} references missing nodes: {missing_text}")
            graph.add_edge(
                edge.source,
                edge.target,
                key=edge.edge_id,
                record=edge,
                capacity=edge.capacity,
                cost=edge.cost_per_unit,
                layer=edge.layer.value,
            )
        return graph

    def shocked_edges(
        self,
        as_of: datetime,
        analysis_cutoff: datetime,
        shocks: Iterable[CapacityShock],
    ) -> list[EdgeRecord]:
        active_shocks = [shock for shock in shocks if shock.active_at(as_of)]
        result: list[EdgeRecord] = []
        for edge in self.active_edges(as_of, analysis_cutoff):
            factor = 1.0
            for shock in active_shocks:
                applies = (
                    (shock.target_type == "edge" and shock.target_id == edge.edge_id)
                    or (
                        shock.target_type == "node"
                        and shock.target_id in {edge.source, edge.target}
                    )
                    or (
                        shock.target_type == "layer"
                        and shock.target_id == edge.layer.value
                    )
                )
                if applies:
                    factor *= shock.capacity_factor
            result.append(edge.model_copy(update={"capacity": edge.capacity * factor}))
        return result
