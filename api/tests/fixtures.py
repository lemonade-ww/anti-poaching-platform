from datetime import datetime

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
def simple_judgment():
    return {
        "title": "A test judgment foo bar with a defendant",
        "content": "asdasdasdasdasd",
        "caseNumber": "A120123",
        "sentence": "asdasd",
        "location": "asdasdasdasd",
        "releaseDate": datetime.now().strftime("%Y-%m-%d"),
        "speciesNames": [],
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


@pytest.fixture
def simple_defendant():
    return {
        "name": "Somebody",
        "gender": "女",
        "educationLevel": "大学",
        "birth": "1980-01-01",
    }
