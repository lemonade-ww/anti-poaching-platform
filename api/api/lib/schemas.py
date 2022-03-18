import datetime
from enum import Enum
from typing import Generic, TypeVar

from fastapi import Depends

from api.lib import APIModel, has_query_params

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


class SpeciesShort(APIModel):
    """
    Species information without taxonomy ranks higher than species
    """

    name: str
    protection_class: ProtectionClass | None = None
    conservation_status: ConservationStatus | None = None


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
    """
    All the constraints need to be satisfied at the same time except fields
    that are unspecified
    """

    species: list[str] | None
    genus: list[str] | None
    family: list[str] | None
    order: list[str] | None
    class_: list[str] | None
    protection_class: list[ProtectionClass] | None
    conservation_status: list[ConservationStatus] | None


# Schema definitions for /analytics/defendant
class Defendant(APIModel):
    """
    Basic information of a defendant
    """

    name: str
    gender: str | None
    birth: datetime.date | None
    education_level: str | None


class BaseDefendantFilter(APIModel):
    name: list[str] | None
    gender: list[str] | None
    birth_before: datetime.datetime | None
    birth_after: datetime.datetime | None
    education_level: list[str] | None


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
    category: list[SourceCategory] | None
    occasion: list[str] | None
    seller: list[str] | None
    buyer: list[str] | None
    method: list[str] | None
    destination: list[str] | None
    usage: list[str] | None


SourcePost = Source

# Schema definitions for /analytics/judgment
class Judgment(APIModel):
    """
    The judgment document
    """

    id: int
    title: str
    content: str | None
    species: list[SpeciesShort]
    defendants: list[Defendant]
    sources: list[Source]


class JudgmentFilter(APIModel):
    judgment_id: int | None
    title: str | None
    location: str | None
    date_before: datetime.datetime | None
    date_after: datetime.datetime | None
    defendant_filter: BaseDefendantFilter = Depends(
        has_query_params(BaseDefendantFilter)
    )
    species_filter: SpeciesFilter = Depends(has_query_params(SpeciesFilter))
    source_filter: SourceFilter = Depends(has_query_params(SourceFilter))


class JudgmentPost(APIModel):
    title: str
    species_names: list[str] = []
    defendants: list[Defendant] = []


class ActionResult(APIModel):
    """
    The result of the current action
    """

    status: ResponseStatus
    message: str | None


class QueryActionResult(ActionResult, Generic[ResultT]):
    result: ResultT
