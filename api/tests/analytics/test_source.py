from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session

from api.crud.judgment import insert_judgment
from api.crud.source import insert_source
from api.db.models import Judgment
from api.lib.schemas import JudgmentPost, SourcePost


def test_post_and_get_source(
    client: TestClient,
    db_session: Session,
    simple_judgment_species: dict,
    simple_source: dict,
    simple_species: dict,
):
    result = client.patch("/analytics/species", json=[simple_species])
    assert result.status_code == 200

    result = client.post("/analytics/judgment", json=simple_judgment_species)
    assert result.status_code == 201

    judgment = (
        db_session.query(Judgment)
        .filter(Judgment.title == simple_judgment_species["title"])
        .first()
    )
    assert judgment is not None
    assert judgment.id is not None
    post_result = client.post(
        f"/analytics/judgment/source/{judgment.id}", json=simple_source
    )
    assert post_result.status_code == 201

    get_result = client.get("/analytics/judgment/source")
    assert get_result.status_code == 200
    assert get_result.json()[0]["buyer"] == simple_source["buyer"]
    assert get_result.json()[0]["method"] == simple_source["method"]


def test_get_source(client: TestClient, db_session: Session, simple_source: dict):
    judgment = insert_judgment(db_session, JudgmentPost(title="test judgment"))
    db_session.add(judgment)
    db_session.flush()
    assert judgment.id is not None
    source = insert_source(db_session, judgment.id, SourcePost(**simple_source))
    db_session.add(source)

    get_result = client.get(
        "/analytics/judgment/source", params=[("buyer", simple_source["buyer"])]
    )
    assert get_result.status_code == 200
    assert get_result.json()[0]["buyer"] == simple_source["buyer"]

    get_result = client.get("/analytics/judgment/source", params=[("buyer", "asd")])
    assert get_result.status_code == 200
    assert len(get_result.json()) == 0


def test_post_source_with_defendant(
    client: TestClient,
    simple_judgment: dict,
    simple_source: dict,
    simple_defendant: dict,
):
    judgment_result = client.post("/analytics/judgment", json=simple_judgment)
    assert judgment_result.status_code == 201
    judgment_id = judgment_result.json()["id"]

    defendant_result = client.post(
        f"/analytics/judgment/defendant/{judgment_id}",
        json=simple_defendant,
    )
    assert defendant_result.status_code == 201
    assert defendant_result.json().get("id") is not None
    defedant_id = defendant_result.json()["id"]

    simple_source["defendantId"] = defendant_result.json()["id"]
    source_result = client.post(
        f"analytics/judgment/source/{judgment_id}", json=simple_source
    )
    assert source_result.status_code == 201
    assert source_result.json()["defendantId"] == defendant_result.json()["id"]

    source_get_result = client.get(
        f"analytics/judgment/source",
        params=[("judgmentId", judgment_id), ("defendantId", defedant_id)],
    )
    source_data = source_get_result.json()[0]
    # category is a enum. We convert it to its value before comparison
    simple_source["category"] = simple_source["category"].value
    # The fixture does not have judgmentId
    del source_data["judgmentId"]
    assert source_data == simple_source
