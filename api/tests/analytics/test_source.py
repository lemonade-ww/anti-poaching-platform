import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session

from api.crud.judgment import insert_judgment
from api.crud.source import insert_source
from api.db.models import Judgment
from api.lib.schemas import ResponseStatus, Source, SourceCategory
from tests.analytics.test_judgment import simple_judgment
from tests.analytics.test_taxon import simple_species


@pytest.fixture
def simple_source():
    return {
        "category": SourceCategory.Buy,
        "seller": "王某某",
        "buyer": "金某某",
        "occasion": "菜市",
        "destination": None,
        "method": None,
        "usage": "食用",
    }


def test_post_and_get_source(
    client: TestClient,
    db_session: Session,
    simple_judgment: dict,
    simple_source: dict,
):
    result = client.post("/analytics/judgment", json=simple_judgment)
    assert result.status_code == 200
    assert result.json()["status"] == ResponseStatus.Success

    judgment = (
        db_session.query(Judgment)
        .filter(Judgment.title == simple_judgment["title"])
        .first()
    )
    assert judgment is not None

    simple_source["judgmentId"] = judgment.id
    assert judgment.id is not None
    post_result = client.post("/analytics/source", json=simple_source)
    assert post_result.status_code == 200

    get_result = client.get("/analytics/source")
    assert get_result.status_code == 200
    assert get_result.json()["result"][0]["buyer"] == simple_source["buyer"]
    assert get_result.json()["result"][0]["method"] == simple_source["method"]


def test_get_source(client: TestClient, db_session: Session, simple_source: dict):
    judgment = insert_judgment(db_session, "test judgment", [])
    db_session.add(judgment)
    db_session.flush()
    assert judgment.id is not None
    simple_source["judgment_id"] = judgment.id
    source = insert_source(db_session, Source(**simple_source))
    db_session.add(source)

    get_result = client.get("/analytics/source", params=[("buyer", "金")])
    assert get_result.status_code == 200
    assert get_result.json()["result"][0]["buyer"] == simple_source["buyer"]

    get_result = client.get("/analytics/source", params=[("buyer", "asd")])
    assert get_result.status_code == 200
    assert len(get_result.json()["result"]) == 0
