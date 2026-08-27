from datetime import UTC, datetime

import pytest

from tsnt.domain.enums import Layer
from tsnt.domain.models import CapacityShock, NodeRecord, ScenarioContract
from tsnt.service.orchestrator import run_network_scenario


def test_network_scenario_compares_baseline_and_shocked_capacity(edge_factory):
    now = datetime(2026, 1, 1, tzinfo=UTC)
    nodes = [
        NodeRecord(
            node_id=node_id,
            name=node_id,
            layer=Layer.TRADE,
            valid_from=now,
            transaction_time=now,
        )
        for node_id in ("s", "a", "t")
    ]
    edges = [
        edge_factory("sa", "s", "a", 10, 1, 2),
        edge_factory("at", "a", "t", 10, 1, 2),
        edge_factory("st", "s", "t", 5, 5, 5),
    ]
    scenario = ScenarioContract(
        scenario_id="demo",
        name="Synthetic",
        as_of=now,
        analysis_cutoff=now,
        shocks=(
            CapacityShock(
                target_type="edge",
                target_id="at",
                capacity_factor=0.5,
                starts_at=now,
                rationale="synthetic",
            ),
        ),
    )
    result = run_network_scenario(nodes, edges, scenario, "s", "t")
    assert result.baseline_max_flow == pytest.approx(15)
    assert result.shocked_max_flow == pytest.approx(10)
    assert result.delta_flow == pytest.approx(-5)
    assert result.confidence == 0.25
