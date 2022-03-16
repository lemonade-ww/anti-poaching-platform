"""Test if the test suite successfully rollback sessions per test case
"""
import pytest
from sqlalchemy.orm.session import Session
from fastapi.testclient import TestClient

from api.crud.judgment import insert_judgment, query_judgment
from api.lib.schemas import DefendantFilter, JudgmentFilter, SourceFilter, SpeciesFilter 

def check_side_effect_crud(db_session: Session, name: str):
    """Create a side-effect that should not persist in any other test cases with a crud module
    """
    judgment = insert_judgment(db_session, name, [])
    db_session.add(judgment)
    db_session.flush()

    # Check if we have successfully inserted it
    judgments = query_judgment(db_session, JudgmentFilter(
        defendant_filter=DefendantFilter(),
        source_filter=SourceFilter(),
        species_filter=SpeciesFilter(),
    ))
    assert len(judgments) == 1

def check_side_effect_client(client: TestClient, name: str):
    """Create a side effect via an endpoint with a test client
    """
    result = client.post("analytics/judgment", json={
        "title": name,
        "speciesNames": [],
    }) 
    assert result.status_code == 200
    
    get_result = client.get("analytics/judgment")
    assert get_result.status_code == 200
    assert len(get_result.json()["result"]) == 1
    assert get_result.json()["result"][0]["title"] == name

def test_side_effect_crud_a(db_session: Session):
    check_side_effect_crud(db_session, "test side effect a")

def test_side_effect_crud_b(db_session: Session):
    check_side_effect_crud(db_session, "test side effect b")

def test_create_side_effect_client_a(client: TestClient):
    check_side_effect_client(client, "test side effect a")

def test_create_side_effect_client_b(client: TestClient):
    check_side_effect_client(client, "test side effect b")
