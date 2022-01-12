import pytest
from fastapi.testclient import TestClient

from api.lib.schemas import ConservationStatus, ProtectionClass


@pytest.fixture
def simple_species():
    return {
        "species": "Emberiza aureola",
        "genus": "Emberiza",
        "family": "Emberizidae",
        "order": "Passeriformes",
        "class": "Aves",
        "protectionClass": ProtectionClass.I,
        "conservationStatus": ConservationStatus.CR,
    }


def test_bulk_put_taxon(client: TestClient, simple_species: dict):
    result = client.patch("/analytics/species", json=[simple_species])

    expected_result = simple_species.copy()
    del expected_result["protectionClass"]
    del expected_result["conservationStatus"]
    expected_result = {key: [val] for key, val in expected_result.items()}
    assert result.json() == expected_result


def test_get_taxon(client: TestClient, simple_species):
    patch_result = client.patch("/analytics/species", json=[simple_species])
    assert patch_result.status_code == 200

    get_result = client.get("/analytics/species")
    assert get_result.status_code == 200
    assert get_result.json()[0] == simple_species
