import pytest

from tsnt.optimization.flow import OptimizationError, max_flow, min_cost_flow


def test_max_flow_preserves_parallel_edges(edge_factory):
    edges = [
        edge_factory("sa-1", "s", "a", 10, 1),
        edge_factory("sa-2", "s", "a", 5, 2),
        edge_factory("at", "a", "t", 12, 1),
        edge_factory("st", "s", "t", 3, 5),
    ]
    result = max_flow(edges, "s", "t")
    assert result.total_flow == pytest.approx(15)
    assert set(result.edge_flows) == {"sa-1", "sa-2", "at", "st"}


def test_min_cost_flow_finds_cheapest_feasible_route(edge_factory):
    edges = [
        edge_factory("sa", "s", "a", 12, 1),
        edge_factory("at", "a", "t", 12, 1),
        edge_factory("st", "s", "t", 3, 5),
    ]
    result = min_cost_flow(edges, "s", "t", 13)
    assert result.total_cost == pytest.approx(29)
    assert result.edge_flows["st"] == pytest.approx(1)


def test_infeasible_min_cost_is_explicit(edge_factory):
    edges = [edge_factory("st", "s", "t", 2, 1)]
    with pytest.raises(OptimizationError):
        min_cost_flow(edges, "s", "t", 3)
