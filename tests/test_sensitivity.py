import pytest

from tsnt.validation.sensitivity import tornado_analysis


def test_tornado_analysis_ranks_largest_normalized_effect():
    def model(parameters):
        return {"output": 2 * parameters["a"] + 3 * parameters["b"]}

    report = tornado_analysis(
        model,
        baseline={"a": 10, "b": 10},
        bounds={"a": (5, 15), "b": (9, 11)},
    )
    assert report.baseline_outputs == {"output": 50}
    assert report.parameter_ranking == ("a", "b")
    effect = next(item for item in report.effects if item.parameter == "a")
    assert effect.absolute_swing == 20
    assert effect.local_elasticity == pytest.approx(0.4)
