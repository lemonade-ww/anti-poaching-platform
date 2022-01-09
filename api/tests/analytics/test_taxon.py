import pytest
from fastapi.testclient import TestClient

from api.utils.enums import ConservationStatus, ProtectionClass


@pytest.fixture
def simple_species():
    return {
        "species": "Emberiza aureola",
        "genus": "Emberiza",
        "family": "Emberizidae",
        "order": "Passeriformes",
        "class_": "Aves",
        "protection_class": ProtectionClass.I,
        "conservation_status": ConservationStatus.CR,
    }


def test_bulk_put_taxon(client: TestClient, simple_species: dict):
    result = client.put("/analytics/species-bulk", json=[simple_species])

    expected_result = simple_species.copy()
    del expected_result["protection_class"]
    del expected_result["conservation_status"]
    expected_result = {key: [val] for key, val in expected_result.items()}
    assert result.json() == expected_result
