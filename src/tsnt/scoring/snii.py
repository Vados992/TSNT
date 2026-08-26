"""SNII scoring with exact decimal arithmetic and deterministic ties."""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from tsnt.domain.models import NodeComponents, NodeRecord

DEFAULT_WEIGHTS: dict[str, Decimal] = {
    "centrality": Decimal("0.25"),
    "throughput": Decimal("0.25"),
    "control": Decimal("0.20"),
    "cascade": Decimal("0.20"),
    "substitutability": Decimal("0.10"),
}


@dataclass(frozen=True, slots=True)
class SNIIScore:
    exact: Decimal
    published: Decimal


def compute_snii(
    components: NodeComponents,
    weights: dict[str, Decimal] | None = None,
    digits: Decimal = Decimal("0.01"),
) -> SNIIScore:
    selected = weights or DEFAULT_WEIGHTS
    if set(selected) != set(DEFAULT_WEIGHTS):
        raise ValueError("weights must contain exactly the five SNII components")
    if sum(selected.values(), Decimal("0")) != Decimal("1"):
        raise ValueError("weights must sum exactly to 1")
    exact = sum(
        Decimal(str(getattr(components, name))) * weight
        for name, weight in selected.items()
    )
    return SNIIScore(exact=exact, published=exact.quantize(digits, rounding=ROUND_HALF_UP))


def rank_nodes(nodes: list[NodeRecord]) -> list[tuple[NodeRecord, SNIIScore]]:
    scored = [(node, compute_snii(node.components)) for node in nodes if node.components]
    return sorted(
        scored,
        key=lambda item: (
            -item[1].exact,
            item[0].components.substitutability if item[0].components else 10,
            -(item[0].components.centrality if item[0].components else 0),
            item[0].name.casefold(),
        ),
    )
