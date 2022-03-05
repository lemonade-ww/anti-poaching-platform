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


class Defendant(APIModel):
    """
    Basic information of a defendant
    """

    name: str
    gender: str | None
    birth: datetime.datetime | None
    education_level: str | None


class Judgment(APIModel):
    """
    The judgment document
    """

    title: str
    species: list[Species]
    defendants: list[Defendant]


class Source(APIModel):
    judgment_id: int
    category: SourceCategory
    occasion: str | None
    seller: str | None
    buyer: str | None
    method: str | None
    destination: str | None
    usage: str | None


class ActionResult(APIModel):
    """
    The result of the current action
    """

    status: ResponseStatus
    message: str | None


class QueryActionResult(ActionResult, Generic[ResultT]):
    result: ResultT
