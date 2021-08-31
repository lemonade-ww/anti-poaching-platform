import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, MutableSequence, Optional, Sequence, TypedDict


with open("src_keywords.json", "r", encoding="utf8") as f:
    SOURCES = json.load(f)


with open("lexicon.json", "r", encoding="utf8") as f:
    LEXICON = json.load(f)


class Source(str, Enum):
    BUY: str = "收购"
    HUNT: str = "猎捕"
    SELL: str = "出售"
    TRANSPORT: str = "运输"


SOURCE_KEY_MAP = {
    Source.BUY: "buy",
    Source.HUNT: "hunt",
    Source.SELL: "sell",
    Source.TRANSPORT: "transport",
}


@dataclass
class SourceInfo:
    type: Source
    occasion: Optional[str] = None
    seller: Optional[str] = None
    buyer: Optional[str] = None
    method: Optional[str] = None
    destination: Optional[str] = None

    def is_empty(self) -> bool:
        return not self.occasion and not self.seller and not self.buyer and not self.method


@dataclass
class SourceData:
    name: str
    input: MutableSequence[SourceInfo] = field(default_factory=list)
    output: MutableSequence[SourceInfo] = field(default_factory=list)


@dataclass
class DefendantData:
    name: str
    gender: Optional[str] = None
    birth: Optional[str] = None
    race: Optional[str] = None
    education_level: Optional[str] = None
    is_valid_person: bool = True
    all_found: bool = False


@dataclass
class PoachingData:
    data_id: str
    defendants: MutableSequence[str] = field(default_factory=list)
    location: str = ""
    defendant_info: MutableSequence[DefendantData] = field(default_factory=list)
    sentence: MutableSequence[str] = field(default_factory=list)
    species_info: Mapping[str, str] = field(default_factory=dict)
    title: Optional[str] = None
    number: Optional[str] = None
    sources_info: MutableSequence[SourceData] = field(default_factory=list)
