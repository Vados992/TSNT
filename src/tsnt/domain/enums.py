"""Controlled vocabularies used across layers."""

from enum import StrEnum


class Layer(StrEnum):
    MARITIME = "maritime"
    TRADE = "trade"
    ENERGY = "energy"
    FINANCE = "finance"
    CABLE = "cable"
    MILITARY = "military"
    LEGAL = "legal"
    INSTITUTIONAL = "institutional"


class EvidenceClass(StrEnum):
    PRIMARY = "primary"
    OFFICIAL = "official"
    COMMERCIAL = "commercial"
    PEER_REVIEWED = "peer_reviewed"
    SECONDARY = "secondary"
    EXPERT_JUDGMENT = "expert_judgment"
    SYNTHETIC = "synthetic"
