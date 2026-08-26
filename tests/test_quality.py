from tsnt.data.quality import QualityGate, UnitRegistry


def test_unit_registry_refuses_cross_dimension_conversion():
    units = UnitRegistry()
    assert units.convert(2, "gw", "mw") == 2_000
    try:
        units.convert(1, "mw", "tonne/day")
    except ValueError as error:
        assert "different dimensions" in str(error)
    else:
        raise AssertionError("cross-dimension conversion should fail")


def test_quality_gate_detects_duplicate_physical_flows(edge_factory):
    first = edge_factory("e1", "s", "t", 1).model_copy(
        update={"canonical_flow_id": "physical-1"}
    )
    second = edge_factory("e2", "s", "t", 1).model_copy(
        update={"canonical_flow_id": "physical-1"}
    )
    report = QualityGate().validate_edges([first, second])
    assert not report.passed
    assert report.issues[0].code == "duplicate_canonical_flow"
