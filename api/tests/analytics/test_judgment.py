from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session

from api.crud.judgment import insert_judgment
from api.db.models import Judgment
from api.lib.schemas import JudgmentPost


def test_post_judgment(client: TestClient, simple_judgment_defendant: dict):
    result = client.post("/analytics/judgment", json=simple_judgment_defendant)
    assert result.status_code == 201
    assert "id" in result.json()

    result = client.get(f'/analytics/judgment/{result.json()["id"]}')
    assert result.json()["defendants"][0] == simple_judgment_defendant["defendants"][0]


def test_post_judgment_with_non_existent_species(
    client: TestClient, simple_judgment_species: dict
):
    result = client.post("/analytics/judgment", json=simple_judgment_species)
    assert result.status_code == 422
    assert (
        result.json()["detail"]
        == f'Resource does not exist: species {simple_judgment_species["speciesNames"][0]}'
    )


def test_post_and_get_judgment(
    client: TestClient,
    db_session: Session,
    simple_judgment_species: dict,
    simple_species: dict,
):
    result = client.patch("/analytics/species", json=[simple_species])
    assert result.status_code == 200

    result = client.post("/analytics/judgment", json=simple_judgment_species)
    assert result.status_code == 201

    judgment: Judgment | None = (
        db_session.query(Judgment)
        .filter(Judgment.title == simple_judgment_species["title"])
        .first()
    )
    assert judgment is not None

    result = client.get("/analytics/judgment", params=[("species", "Emberiza aureola")])
    assert result.status_code == 200
    assert len(result.json()) == 1
    assert result.json()[0]["title"] == simple_judgment_species["title"]
    assert result.json()[0]["id"] == judgment.id


def test_get_single_judgment(
    client: TestClient,
    db_session: Session,
    simple_judgment_defendant: dict,
):
    judgment = insert_judgment(
        db_session, JudgmentPost.parse_obj(simple_judgment_defendant)
    )
    db_session.add(judgment)
    db_session.commit()

    result = client.get(f"/analytics/judgment/{judgment.id}")
    assert result.status_code == 200
    assert result.json()["title"] == simple_judgment_defendant["title"]
    assert result.json()["id"] == judgment.id


def test_get_nonexistent_judgment(
    client: TestClient,
):
    result = client.get("/analytics/judgment/100")
    assert result.status_code == 404
    assert result.json()["detail"] == "Resource does not exist: judgment 100"
