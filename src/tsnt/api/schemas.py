"""Public API request and response contracts."""

from pydantic import BaseModel, ConfigDict, Field

from tsnt.domain.models import EdgeRecord, NodeComponents, NodeRecord, ScenarioContract


class StrictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SNIIRequest(StrictRequest):
    components: NodeComponents


class FlowRequest(StrictRequest):
    edges: list[EdgeRecord] = Field(min_length=1)
    source: str
    sink: str


class MinCostFlowRequest(FlowRequest):
    required_flow: float = Field(ge=0)


class LeontiefRequest(StrictRequest):
    coefficients: list[list[float]]
    final_demand: list[float]


class CascadeRequest(StrictRequest):
    influence: list[list[float]]
    initial_shock: list[float]
    threshold: float = Field(default=0.5, ge=0, le=1)
    max_steps: int = Field(default=100, ge=1, le=10_000)


class NetworkScenarioRequest(StrictRequest):
    nodes: list[NodeRecord] = Field(min_length=2)
    edges: list[EdgeRecord] = Field(min_length=1)
    scenario: ScenarioContract
    source: str
    sink: str
