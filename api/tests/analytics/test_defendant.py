import datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session

from api.crud.defendant import insert_defendant
from api.crud.judgment import query_judgment
from api.db.models import Judgment
from api.lib.errors import check_not_none
from api.lib.schemas import JudgmentFilter


def test_get_defendant(
    client: TestClient,
    db_session: Session,
    simple_judgment: dict,
):
    # Insert the simple judgment first
    result = client.post("/analytics/judgment", json=simple_judgment)
    assert result.status_code == 201

    # Ensure that the judgment is inserted
    judgments: list[Judgment] = query_judgment(
        db_session,
        JudgmentFilter.no_depends(
            title=simple_judgment["title"],
        ),
    )

    assert len(judgments) > 0

    insert_defendant(
        db_session,
        check_not_none(judgments[0].id, "id"),
        "Test",
        "M",
        datetime.datetime.now(),
        "High School",
    )

    result = client.get(
        "/analytics/judgment/defendant",
        params={
            "name": "Test",
        },
    )
    assert result.status_code == 200
    assert len(result.json()) > 0
    assert result.json()[0]["gender"] == "M"


def test_post_defendant(
    client: TestClient,
    simple_judgment_species: dict,
    simple_species: dict,
    simple_defendant: dict,
):
    result = client.patch("/analytics/species", json=[simple_species])
    assert result.status_code == 200

    result = client.post("/analytics/judgment", json=simple_judgment_species)
    assert result.status_code == 201
    judgment_id = result.json()["id"]
    assert judgment_id is not None

    result = client.post(
        f"/analytics/judgment/defendant/{judgment_id}", json=simple_defendant
    )
    result_json = result.json()
    del result_json["id"]
    assert result_json == simple_defendant
    assert result.status_code == 201


def test_add_defendant_to_nonexistent_judgment(
    client: TestClient,
    simple_defendant: dict,
):
    result = client.post("/analytics/judgment/defendant/1", json=simple_defendant)
    assert result.status_code == 422
    assert result.json()["detail"] == "Resource does not exist: judgment 1"
