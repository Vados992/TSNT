"""Linear-programming flow solvers preserving parallel-edge identity."""

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from scipy.optimize import linprog

from tsnt.domain.models import EdgeRecord


class OptimizationError(RuntimeError):
    """Raised when a scenario is infeasible or the solver fails."""


@dataclass(frozen=True, slots=True)
class FlowResult:
    total_flow: float
    total_cost: float
    edge_flows: dict[str, float]
    solver_status: str


def _prepare(edges: Sequence[EdgeRecord]) -> tuple[list[str], dict[str, int]]:
    edge_ids = [edge.edge_id for edge in edges]
    if len(edge_ids) != len(set(edge_ids)):
        raise ValueError("edge_id values must be unique")
    nodes = sorted({value for edge in edges for value in (edge.source, edge.target)})
    return nodes, {node: index for index, node in enumerate(nodes)}


def max_flow(edges: Sequence[EdgeRecord], source: str, sink: str) -> FlowResult:
    """Maximise source-to-sink flow under edge capacities."""
    if source == sink:
        raise ValueError("source and sink must differ")
    nodes, node_index = _prepare(edges)
    if source not in node_index or sink not in node_index:
        raise ValueError("source and sink must occur in the edge set")

    edge_count = len(edges)
    objective = np.zeros(edge_count + 1)
    objective[-1] = -1.0
    balance = np.zeros((len(nodes), edge_count + 1))
    for index, edge in enumerate(edges):
        balance[node_index[edge.source], index] += 1.0
        balance[node_index[edge.target], index] -= 1.0
    balance[node_index[source], -1] = -1.0
    balance[node_index[sink], -1] = 1.0

    result = linprog(
        objective,
        A_eq=balance,
        b_eq=np.zeros(len(nodes)),
        bounds=[(0.0, edge.capacity) for edge in edges] + [(0.0, None)],
        method="highs",
    )
    if not result.success:
        raise OptimizationError(f"max-flow optimization failed: {result.message}")
    flows = {edge.edge_id: float(result.x[index]) for index, edge in enumerate(edges)}
    return FlowResult(
        total_flow=float(result.x[-1]),
        total_cost=float(
            sum(flows[edge.edge_id] * edge.cost_per_unit for edge in edges)
        ),
        edge_flows=flows,
        solver_status=result.message,
    )


def min_cost_flow(
    edges: Sequence[EdgeRecord],
    source: str,
    sink: str,
    required_flow: float,
) -> FlowResult:
    """Route an exact feasible quantity at minimum variable cost."""
    if required_flow < 0:
        raise ValueError("required_flow cannot be negative")
    if source == sink:
        raise ValueError("source and sink must differ")
    nodes, node_index = _prepare(edges)
    if source not in node_index or sink not in node_index:
        raise ValueError("source and sink must occur in the edge set")

    balance = np.zeros((len(nodes), len(edges)))
    for index, edge in enumerate(edges):
        balance[node_index[edge.source], index] += 1.0
        balance[node_index[edge.target], index] -= 1.0
    demand = np.zeros(len(nodes))
    demand[node_index[source]] = required_flow
    demand[node_index[sink]] = -required_flow

    result = linprog(
        np.array([edge.cost_per_unit for edge in edges]),
        A_eq=balance,
        b_eq=demand,
        bounds=[(0.0, edge.capacity) for edge in edges],
        method="highs",
    )
    if not result.success:
        raise OptimizationError(f"min-cost optimization failed: {result.message}")
    flows = {edge.edge_id: float(result.x[index]) for index, edge in enumerate(edges)}
    return FlowResult(
        total_flow=required_flow,
        total_cost=float(result.fun),
        edge_flows=flows,
        solver_status=result.message,
    )
