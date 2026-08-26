"""External data connector contract."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from tsnt.data.provenance import ProvenanceRecord
from tsnt.domain.models import EdgeRecord, NodeRecord


class DataAccessError(RuntimeError):
    """Raised when authorised access or licensing is missing."""


@dataclass(frozen=True, slots=True)
class IngestionBatch:
    nodes: tuple[NodeRecord, ...]
    edges: tuple[EdgeRecord, ...]
    provenance: ProvenanceRecord


class IngestionAdapter(ABC):
    @abstractmethod
    def fetch(self, valid_from: datetime, valid_to: datetime) -> IngestionBatch:
        """Return a provenance-bound batch for a requested valid-time window."""
