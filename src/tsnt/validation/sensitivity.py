"""Deterministic one-at-a-time sensitivity analysis."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True, slots=True)
class SensitivityEffect:
    parameter: str
    output: str
    low_input: float
    high_input: float
    baseline_output: float
    low_output: float
    high_output: float
    absolute_swing: float
    local_elasticity: float | None


@dataclass(frozen=True, slots=True)
class SensitivityReport:
    baseline_outputs: dict[str, float]
    effects: tuple[SensitivityEffect, ...]
    parameter_ranking: tuple[str, ...]


SensitivityModel = Callable[[Mapping[str, float]], float | Mapping[str, float]]


def _outputs(raw: float | Mapping[str, float]) -> dict[str, float]:
    values = {"value": float(raw)} if isinstance(raw, (int, float)) else {
        name: float(value) for name, value in raw.items()
    }
    if not values or not all(isfinite(value) for value in values.values()):
        raise ValueError("sensitivity model must return a non-empty set of finite outputs")
    return values


def tornado_analysis(
    model: SensitivityModel,
    baseline: Mapping[str, float],
    bounds: Mapping[str, tuple[float, float]],
) -> SensitivityReport:
    """Vary each bounded parameter alone and rank its normalized output swing."""
    parameters = {name: float(value) for name, value in baseline.items()}
    if not parameters or not all(isfinite(value) for value in parameters.values()):
        raise ValueError("baseline parameters must be finite and non-empty")
    if set(bounds) != set(parameters):
        raise ValueError("bounds must be supplied for every baseline parameter")

    baseline_outputs = _outputs(model(parameters))
    effects: list[SensitivityEffect] = []
    aggregate: dict[str, float] = {}
    for name, base_value in parameters.items():
        low, high = (float(value) for value in bounds[name])
        if not (isfinite(low) and isfinite(high) and low <= base_value <= high):
            raise ValueError(f"invalid bounds for {name}")
        low_parameters = {**parameters, name: low}
        high_parameters = {**parameters, name: high}
        low_outputs = _outputs(model(low_parameters))
        high_outputs = _outputs(model(high_parameters))
        if set(low_outputs) != set(baseline_outputs) or set(high_outputs) != set(
            baseline_outputs
        ):
            raise ValueError("model output keys changed during sensitivity analysis")

        score = 0.0
        for output, base_output in baseline_outputs.items():
            low_output = low_outputs[output]
            high_output = high_outputs[output]
            swing = abs(high_output - low_output)
            input_fraction = (
                (high - low) / abs(base_value) if base_value != 0 else None
            )
            output_fraction = (
                (high_output - low_output) / abs(base_output)
                if base_output != 0
                else None
            )
            elasticity = (
                output_fraction / input_fraction
                if input_fraction not in (None, 0) and output_fraction is not None
                else None
            )
            scale = abs(base_output) if base_output != 0 else 1.0
            score += swing / scale
            effects.append(
                SensitivityEffect(
                    parameter=name,
                    output=output,
                    low_input=low,
                    high_input=high,
                    baseline_output=base_output,
                    low_output=low_output,
                    high_output=high_output,
                    absolute_swing=swing,
                    local_elasticity=elasticity,
                )
            )
        aggregate[name] = score

    ranking = tuple(sorted(aggregate, key=lambda name: (-aggregate[name], name)))
    return SensitivityReport(baseline_outputs, tuple(effects), ranking)
