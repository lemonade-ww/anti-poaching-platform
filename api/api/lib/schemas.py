import datetime
from enum import Enum
from typing import Generic, TypeVar

from api.lib import APIModel

ResultT = TypeVar("ResultT")


class ConservationStatus(str, Enum):
    EX = "EX"  # Extinct
    EW = "EW"  # Extinct in the wild
    CR = "CR"  # Critically endangered
    EN = "EN"  # Endangered
    VU = "VU"  # Vulnerable
    NT = "NT"  # Near threatened
    CD = "CD"  # Conservation Dependent
    LC = "LC"  # Least concern
    DD = "DD"  # Data deficient
    NE = "NE"  # Not evaluated


class ProtectionClass(str, Enum):
    I = "I"
    II = "II"


class SourceCategory(str, Enum):
    Buy = "收购"
    Hunt = "猎捕"
    Sell = "出售"
    Transport = "运输"


class ResponseStatus(str, Enum):
    Success = "success"
    Pending = "pending"
    Error = "error"


# Schema definitions for /analytics/species
class Species(APIModel):
    """
    Defines a species catagorized by the taxonomy ranks
    """

    species: str
    genus: str
    family: str
    order: str
    class_: str
    protection_class: ProtectionClass | None = None
    conservation_status: ConservationStatus | None = None
    __slots__ = "__weakref__"


class SpeciesBulkPatchResult(APIModel):
    """
    The taxons inserted or updated
    """

    species: list[str] = []
    genus: list[str] = []
    family: list[str] = []
    order: list[str] = []
    class_: list[str] = []


class SpeciesFilter(APIModel):
    species: str | None
    genus: str | None
    family: str | None
    order: str | None
    class_: str | None


# Schema definitions for /analytics/defendant
class Defendant(APIModel):
    """
    Basic information of a defendant
    """

    name: str
    gender: str | None
    birth: datetime.datetime | None
    education_level: str | None


class BaseDefendantFilter(APIModel):
    name: str | None
    gender: str | None
    birth_before: datetime.datetime | None
    birth_after: datetime.datetime | None
    education_level: str | None


class DefendantFilter(BaseDefendantFilter):
    judgment_id: int | None


class DefendantPost(APIModel):
    name: str
    judgment_id: int
    gender: str | None
    birth: datetime.datetime | None
    education_level: str | None


# Schema definitions for /analytics/source
class Source(APIModel):
    judgment_id: int
    category: SourceCategory
    occasion: str | None
    seller: str | None
    buyer: str | None
    method: str | None
    destination: str | None
    usage: str | None


class SourceFilter(APIModel):
    judgment_id: int | None
    category: SourceCategory | None
    occasion: str | None
    seller: str | None
    buyer: str | None
    method: str | None
    destination: str | None
    usage: str | None


SourcePost = Source

# Schema definitions for /analytics/judgment
class Judgment(APIModel):
    """
    The judgment document
    """

    title: str
    species: list[Species]
    defendants: list[Defendant]


class JudgmentFilter(APIModel):
    title: str | None
    location: str | None
    year: datetime.datetime | None
    defendant_filter: BaseDefendantFilter | None
    species_filter: SpeciesFilter | None
    sources_filter: SourceFilter | None


class JudgmentPost(APIModel):
    title: str
    species_names: list[str]
    defendants: list[Defendant] = []


class ActionResult(APIModel):
    """
    The result of the current action
    """

    status: ResponseStatus
    message: str | None


class QueryActionResult(ActionResult, Generic[ResultT]):
    result: ResultT
