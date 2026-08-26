"""Versioned analytical endpoints."""

from dataclasses import asdict
from typing import Any

import numpy as np
from fastapi import APIRouter, HTTPException

from tsnt.api.schemas import (
    CascadeRequest,
    FlowRequest,
    LeontiefRequest,
    MinCostFlowRequest,
    NetworkScenarioRequest,
    SNIIRequest,
)
from tsnt.cascade.engine import simulate_cascade
from tsnt.economics.input_output import leontief_output
from tsnt.optimization.flow import OptimizationError, max_flow, min_cost_flow
from tsnt.scoring.snii import compute_snii
from tsnt.service.orchestrator import run_network_scenario

router = APIRouter(prefix="/v1")


def _flow_payload(result: Any) -> dict[str, Any]:
    return {
        "total_flow": result.total_flow,
        "total_cost": result.total_cost,
        "edge_flows": result.edge_flows,
        "solver_status": result.solver_status,
    }


@router.post("/scoring/snii")
def score_snii(request: SNIIRequest) -> dict[str, str]:
    score = compute_snii(request.components)
    return {"exact": str(score.exact), "published": str(score.published)}


@router.post("/flows/max")
def solve_max_flow(request: FlowRequest) -> dict[str, Any]:
    try:
        return _flow_payload(max_flow(request.edges, request.source, request.sink))
    except (ValueError, OptimizationError) as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.post("/flows/min-cost")
def solve_min_cost(request: MinCostFlowRequest) -> dict[str, Any]:
    try:
        result = min_cost_flow(
            request.edges,
            request.source,
            request.sink,
            request.required_flow,
        )
        return _flow_payload(result)
    except (ValueError, OptimizationError) as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.post("/economics/leontief")
def solve_leontief(request: LeontiefRequest) -> dict[str, Any]:
    try:
        result = leontief_output(
            np.asarray(request.coefficients),
            np.asarray(request.final_demand),
        )
        return {
            "gross_output": result.gross_output.tolist(),
            "spectral_radius": result.spectral_radius,
            "condition_number": result.condition_number,
        }
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.post("/cascades/simulate")
def cascade(request: CascadeRequest) -> dict[str, Any]:
    try:
        result = simulate_cascade(
            np.asarray(request.influence),
            np.asarray(request.initial_shock),
            request.threshold,
            request.max_steps,
        )
        payload = asdict(result)
        payload["final_state"] = result.final_state.tolist()
        payload["history"] = [state.tolist() for state in result.history]
        return payload
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.post("/scenarios/network")
def network_scenario(request: NetworkScenarioRequest) -> dict[str, Any]:
    try:
        result = run_network_scenario(
            request.nodes,
            request.edges,
            request.scenario,
            request.source,
            request.sink,
        )
        return result.model_dump(mode="json")
    except (ValueError, OptimizationError) as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
