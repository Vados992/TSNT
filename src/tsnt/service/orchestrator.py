"""Pure orchestration joining temporal selection, shocks and routing models."""

from pydantic import BaseModel, ConfigDict

from tsnt.data.quality import QualityGate
from tsnt.domain.enums import EvidenceClass
from tsnt.domain.models import EdgeRecord, NodeRecord, ScenarioContract
from tsnt.graph.temporal import TemporalMultiLayerGraph
from tsnt.optimization.flow import max_flow, min_cost_flow


class NetworkScenarioResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    scenario_id: str
    baseline_max_flow: float
    shocked_max_flow: float
    delta_flow: float
    comparable_flow: float
    baseline_cost: float
    shocked_cost: float
    delta_cost: float
    baseline_transit_days: float
    shocked_transit_days: float
    delta_transit_days: float
    confidence: float
    random_seed: int


_EVIDENCE_CONFIDENCE = {
    EvidenceClass.PRIMARY: 0.95,
    EvidenceClass.OFFICIAL: 0.90,
    EvidenceClass.COMMERCIAL: 0.85,
    EvidenceClass.PEER_REVIEWED: 0.90,
    EvidenceClass.SECONDARY: 0.65,
    EvidenceClass.EXPERT_JUDGMENT: 0.50,
    EvidenceClass.SYNTHETIC: 0.25,
}


def _weighted_time(edges: list[EdgeRecord], flows: dict[str, float], total: float) -> float:
    if total == 0:
        return 0.0
    return sum(
        flows.get(edge.edge_id, 0.0) * edge.transit_time_days for edge in edges
    ) / total


def run_network_scenario(
    nodes: list[NodeRecord],
    edges: list[EdgeRecord],
    scenario: ScenarioContract,
    source: str,
    sink: str,
) -> NetworkScenarioResult:
    QualityGate().require_edges(edges)
    graph = TemporalMultiLayerGraph(nodes, edges)
    graph.snapshot(scenario.as_of, scenario.analysis_cutoff)
    baseline_edges = graph.active_edges(scenario.as_of, scenario.analysis_cutoff)
    shocked_edges = graph.shocked_edges(
        scenario.as_of,
        scenario.analysis_cutoff,
        scenario.shocks,
    )
    baseline_max = max_flow(baseline_edges, source, sink)
    shocked_max = max_flow(shocked_edges, source, sink)
    comparable = min(baseline_max.total_flow, shocked_max.total_flow)
    baseline_route = min_cost_flow(baseline_edges, source, sink, comparable)
    shocked_route = min_cost_flow(shocked_edges, source, sink, comparable)
    confidence_values = [_EVIDENCE_CONFIDENCE[edge.evidence_class] for edge in baseline_edges]
    confidence = min(confidence_values) if confidence_values else 0.0
    baseline_time = _weighted_time(baseline_edges, baseline_route.edge_flows, comparable)
    shocked_time = _weighted_time(shocked_edges, shocked_route.edge_flows, comparable)
    return NetworkScenarioResult(
        scenario_id=scenario.scenario_id,
        baseline_max_flow=baseline_max.total_flow,
        shocked_max_flow=shocked_max.total_flow,
        delta_flow=shocked_max.total_flow - baseline_max.total_flow,
        comparable_flow=comparable,
        baseline_cost=baseline_route.total_cost,
        shocked_cost=shocked_route.total_cost,
        delta_cost=shocked_route.total_cost - baseline_route.total_cost,
        baseline_transit_days=baseline_time,
        shocked_transit_days=shocked_time,
        delta_transit_days=shocked_time - baseline_time,
        confidence=confidence,
        random_seed=scenario.random_seed,
    )
