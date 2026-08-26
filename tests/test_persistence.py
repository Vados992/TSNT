from datetime import UTC, datetime

from sqlalchemy.orm import Session

from tsnt.domain.enums import Layer
from tsnt.domain.models import NodeRecord
from tsnt.persistence.database import create_schema, make_engine
from tsnt.persistence.repository import GraphRepository


def test_node_version_roundtrip_in_sqlite():
    engine = make_engine("sqlite+pysqlite:///:memory:")
    create_schema(engine)
    now = datetime(2026, 1, 1, tzinfo=UTC)
    node = NodeRecord(
        node_id="demo",
        name="Demo",
        layer=Layer.TRADE,
        valid_from=now,
        transaction_time=now,
    )
    with Session(engine) as session:
        repository = GraphRepository(session)
        repository.add_node(node)
        session.commit()
        loaded = repository.visible_nodes(now, now)
    assert loaded == [node]
