import pytest

from tsnt.uncertainty.monte_carlo import run_monte_carlo


def test_monte_carlo_is_reproducible_and_reports_quantiles():
    def sampler(rng):
        return {"x": rng.normal(10, 2)}

    def model(parameters):
        return {"loss": max(0.0, parameters["x"] - 8)}

    first = run_monte_carlo(sampler, model, 1_000, seed=42, exceedance_thresholds={"loss": 3})
    second = run_monte_carlo(sampler, model, 1_000, seed=42, exceedance_thresholds={"loss": 3})
    assert first == second
    summary = first.outputs["loss"]
    assert summary.p10 <= summary.p50 <= summary.p90
    assert summary.exceedance_probability == pytest.approx(
        second.outputs["loss"].exceedance_probability
    )
