"""Repository translating validated domain records into versioned rows."""

import hashlib
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from tsnt.domain.models import EdgeRecord, NodeRecord
from tsnt.persistence.models import EdgeVersion, NodeVersion


def _version_id(kind: str, record_id: str, transaction_time: datetime) -> str:
    value = f"{kind}:{record_id}:{transaction_time.isoformat()}".encode()
    return hashlib.sha256(value).hexdigest()


class GraphRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_node(self, node: NodeRecord) -> str:
        version_id = _version_id("node", node.node_id, node.transaction_time)
        self.session.merge(
            NodeVersion(
                version_id=version_id,
                node_id=node.node_id,
                valid_from=node.valid_from,
                valid_to=node.valid_to,
                transaction_time=node.transaction_time,
                payload=node.model_dump(mode="json"),
            )
        )
        return version_id

    def add_edge(self, edge: EdgeRecord) -> str:
        version_id = _version_id("edge", edge.edge_id, edge.transaction_time)
        self.session.merge(
            EdgeVersion(
                version_id=version_id,
                edge_id=edge.edge_id,
                source=edge.source,
                target=edge.target,
                capacity=edge.capacity,
                valid_from=edge.valid_from,
                valid_to=edge.valid_to,
                transaction_time=edge.transaction_time,
                payload=edge.model_dump(mode="json"),
            )
        )
        return version_id

    def visible_nodes(self, as_of: datetime, cutoff: datetime) -> list[NodeRecord]:
        query = select(NodeVersion).where(
            NodeVersion.valid_from <= as_of,
            (NodeVersion.valid_to.is_(None) | (NodeVersion.valid_to > as_of)),
            NodeVersion.transaction_time <= cutoff,
        )
        return [NodeRecord.model_validate(row.payload) for row in self.session.scalars(query)]

    def visible_edges(self, as_of: datetime, cutoff: datetime) -> list[EdgeRecord]:
        query = select(EdgeVersion).where(
            EdgeVersion.valid_from <= as_of,
            (EdgeVersion.valid_to.is_(None) | (EdgeVersion.valid_to > as_of)),
            EdgeVersion.transaction_time <= cutoff,
        )
        return [EdgeRecord.model_validate(row.payload) for row in self.session.scalars(query)]
