"""Safe integration seams for licensed or protected feeds.

These classes deliberately do not emulate data. A deployment supplies a reviewed
client implementation and credentials under the applicable data licence.
"""

from dataclasses import dataclass
from datetime import datetime
from os import getenv

from tsnt.ingestion.base import DataAccessError, IngestionAdapter, IngestionBatch


@dataclass(frozen=True, slots=True)
class ConnectorSpecification:
    name: str
    credential_environment_variable: str
    expected_fields: tuple[str, ...]


class CredentialledConnector(IngestionAdapter):
    specification: ConnectorSpecification

    def fetch(self, valid_from: datetime, valid_to: datetime) -> IngestionBatch:
        credential = getenv(self.specification.credential_environment_variable)
        if not credential:
            raise DataAccessError(
                f"{self.specification.name} requires authorised credentials in "
                f"{self.specification.credential_environment_variable}"
            )
        raise NotImplementedError(
            f"configure a licensed {self.specification.name} client for this deployment"
        )


class AISConnector(CredentialledConnector):
    specification = ConnectorSpecification(
        "AIS",
        "TSNT_AIS_API_KEY",
        ("mmsi", "timestamp", "latitude", "longitude", "draught", "destination"),
    )


class TradeConnector(CredentialledConnector):
    specification = ConnectorSpecification(
        "trade",
        "TSNT_TRADE_API_KEY",
        ("period", "reporter", "partner", "commodity", "value", "quantity", "unit"),
    )


class EnergyConnector(CredentialledConnector):
    specification = ConnectorSpecification(
        "energy",
        "TSNT_ENERGY_API_KEY",
        ("timestamp", "asset", "commodity", "flow", "capacity", "unit"),
    )


class FinanceConnector(CredentialledConnector):
    specification = ConnectorSpecification(
        "finance",
        "TSNT_FINANCE_API_KEY",
        ("timestamp", "instrument", "venue", "currency", "value"),
    )


class CableConnector(CredentialledConnector):
    specification = ConnectorSpecification(
        "cable",
        "TSNT_CABLE_DATA_KEY",
        ("segment", "landing_point", "capacity", "status", "effective_time"),
    )
