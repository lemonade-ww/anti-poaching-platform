import datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session

from api.crud.defendant import insert_defendant, query_defendant
from api.crud.judgment import query_judgment
from api.db.models import Judgment
from api.lib.errors import check_not_none
from api.lib.schemas import DefendantFilter, DefendantPost, JudgmentFilter


def test_get_defendant(
    client: TestClient,
    db_session: Session,
    simple_judgment_defendant: dict,
):
    # Insert the simple judgment first
    result = client.post("/analytics/judgment", json=simple_judgment_defendant)
    assert result.status_code == 201

    # Ensure that the judgment is inserted
    judgments: list[Judgment] = query_judgment(
        db_session,
        JudgmentFilter.no_depends(
            title=simple_judgment_defendant["title"],
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
        "/analytics/defendant",
        params={
            "name": "Test",
        },
    )
    assert result.status_code == 200
    assert len(result.json()) > 0
    assert result.json()[0]["gender"] == "M"


def test_add_defendant_through_post_judgment(
    client: TestClient,
    db_session: Session,
    simple_judgment_defendant: dict,
):
    result = client.post("/analytics/judgment", json=simple_judgment_defendant)
    assert result.status_code == 201

    defendants = query_defendant(db_session, DefendantFilter(name=["ASD"]))
    assert len(defendants) > 0
    assert defendants is not None

    result = client.get("/analytics/defendant")
    expected_defendant = simple_judgment_defendant["defendants"][0]
    assert result.status_code == 200
    assert result.json()[0]["name"] == expected_defendant["name"]
    assert result.json()[0]["educationLevel"] == expected_defendant["educationLevel"]


def test_add_defendant_to_nonexistent_judgment(
    client: TestClient,
    simple_defendant: dict,
):
    simple_defendant["judgment_id"] = 1
    result = client.post("/analytics/defendant", json=simple_defendant)
    assert result.status_code == 422
    assert result.json()["detail"] == "Resource does not exist: judgment 1"
