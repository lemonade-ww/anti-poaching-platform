import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session

from api.db.models import Judgment
from api.lib.schemas import ResponseStatus
from tests.analytics.test_taxon import simple_species


@pytest.fixture
def simple_judgment(simple_species: dict):
    return {
        "title": "A test judgment foo bar",
        "speciesNames": [simple_species["species"]],
    }


def test_post_and_get_judgment(
    client: TestClient,
    db_session: Session,
    simple_judgment: dict,
    simple_species: dict,
):
    result = client.patch("/analytics/species", json=[simple_species])
    assert result.status_code == 200

    result = client.post("/analytics/judgment", json=simple_judgment)
    assert result.status_code == 200
    assert result.json()["status"] == ResponseStatus.Success

    judgment: Judgment | None = (
        db_session.query(Judgment)
        .filter(Judgment.title == simple_judgment["title"])
        .first()
    )
    assert judgment is not None

    result = client.get("/analytics/judgment", params=[("species", "Emberiza aureola")])
    assert result.status_code == 200
    assert len(result.json()["result"]) == 1
    assert result.json()["result"][0]["title"] == simple_judgment["title"]
    assert result.json()["result"][0]["id"] == judgment.id
