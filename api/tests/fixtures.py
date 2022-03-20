import pytest
from sqlalchemy.orm.session import Session

from api.lib.schemas import ConservationStatus, ProtectionClass, SourceCategory


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


@pytest.fixture
def simple_judgment_species(simple_species: dict):
    return {
        "title": "A test judgment foo bar",
        "speciesNames": [simple_species["species"]],
    }


@pytest.fixture
def simple_judgment_defendant():
    return {
        "title": "A test judgment foo bar with a defendant",
        "speciesNames": [],
        "defendants": [
            {
                "name": "ASD",
                "gender": "男",
                "educationLevel": "高中",
                "birth": "1980-01-01",
            }
        ],
    }


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
