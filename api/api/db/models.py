from typing import List, Type, TypeVar

from sqlalchemy import Date, Enum, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.decl_api import declared_attr
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime

from api.lib import to_snake
from api.lib.schemas import ConservationStatus, ProtectionClass, SourceCategory


class CustomBase(object):
    @declared_attr
    def __tablename__(cls):
        return to_snake(cls.__name__)


class IdMixin(object):
    id = Column(Integer, primary_key=True, autoincrement=True)


Base = declarative_base(cls=CustomBase)
BaseT = TypeVar("BaseT", bound=Base)
ModelT = Type[BaseT]


class TaxonClass(Base, IdMixin):
    name = Column(String(255), nullable=False, unique=True)

    orders: List["TaxonOrder"] = relationship("TaxonOrder", back_populates="class_")


class TaxonOrder(Base, IdMixin):
    name = Column(String(255), nullable=False, unique=True)
    class_id = Column(Integer, ForeignKey(TaxonClass.id), nullable=False)

    families: List["TaxonFamily"] = relationship("TaxonFamily", back_populates="order")
    class_: TaxonClass = relationship(TaxonClass, back_populates="orders")


class TaxonFamily(Base, IdMixin):
    name = Column(String(255), nullable=False, unique=True)
    order_id = Column(Integer, ForeignKey(TaxonOrder.id), nullable=False)

    genuses: List["TaxonGenus"] = relationship("TaxonGenus", back_populates="family")
    order: TaxonOrder = relationship(TaxonOrder, back_populates="families")


class TaxonGenus(Base, IdMixin):
    name = Column(String(255), nullable=False, unique=True)
    family_id = Column(Integer, ForeignKey(TaxonFamily.id), nullable=False)

    species: List["TaxonSpecies"] = relationship("TaxonSpecies", back_populates="genus")
    family: TaxonFamily = relationship(TaxonFamily, back_populates="genuses")


judgment_species = Table(
    "judgment_species",
    Base.metadata,
    Column("species_id", ForeignKey("taxon_species.id"), primary_key=True),
    Column("judgment_id", ForeignKey("judgment.id"), primary_key=True),
)


class TaxonSpecies(Base, IdMixin):
    name = Column(String(255), nullable=False, unique=True)
    genus_id = Column(Integer, ForeignKey(TaxonGenus.id), nullable=False)

    protection_class = Column(Enum(ProtectionClass))
    conservation_status = Column(Enum(ConservationStatus))

    judgments: list["Judgment"] = relationship(
        "Judgment", secondary=judgment_species, back_populates="species"
    )
    genus: TaxonGenus = relationship(TaxonGenus, back_populates="species")


class Defendant(Base, IdMixin):
    name = Column(String(255))
    gender = Column(String(1))
    birth = Column(Date)
    education_level = Column(String(20))
    judgment_id = Column(Integer, ForeignKey("judgment.id"), nullable=False)

    judgment: "Judgment" = relationship("Judgment", back_populates="defendants")


class Source(Base, IdMixin):
    category = Column(Enum(SourceCategory), nullable=False)
    occasion = Column(String(255))
    seller = Column(String(255))
    buyer = Column(String(255))
    method = Column(String(255))
    destination = Column(String(255))
    usage = Column(String(255))

    judgment_id = Column(Integer, ForeignKey("judgment.id"), nullable=False)
    judgment: "Judgment" = relationship("Judgment", back_populates="sources")


class Judgment(Base, IdMixin):
    """
    A complete judgment document with meta data
    """

    title = Column(String())
    case_number = Column(String())  # 案号

    location = Column(String())
    release_date = Column(Date)
    creation_time = Column(DateTime, server_default=func.now())
    content = Column(Text())
    sentence = Column(Text())

    species: list[TaxonSpecies] = relationship(
        TaxonSpecies,
        secondary=judgment_species,
        back_populates="judgments",
        uselist=True,
    )
    defendants: list[Defendant] = relationship("Defendant", back_populates="judgment")
    sources: list[Source] = relationship("Source", back_populates="judgment")
