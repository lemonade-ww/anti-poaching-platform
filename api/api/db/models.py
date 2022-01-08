from typing import List, Type, TypeVar

from sqlalchemy import Enum, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey

from api.utils.enums import ConservationStatus, ProtectionClass

Base = declarative_base()
BaseT = TypeVar("BaseT", bound=Base)
ModelT = Type[BaseT]


class TaxonClass(Base):
    __tablename__ = "taxon_class"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(12), nullable=False, unique=True)

    orders: List["TaxonOrder"] = relationship("TaxonOrder", backref="class_")


class TaxonOrder(Base):
    __tablename__ = "taxon_order"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(12), nullable=False, unique=True)
    class_id = Column(Integer, ForeignKey(TaxonClass.id), nullable=False)

    families: List["TaxonFamily"] = relationship("TaxonFamily", backref="order")


class TaxonFamily(Base):
    __tablename__ = "taxon_family"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(12), nullable=False, unique=True)
    order_id = Column(Integer, ForeignKey(TaxonOrder.id), nullable=False)

    genuses: List["TaxonGenus"] = relationship("TaxonGenus", backref="family")


class TaxonGenus(Base):
    __tablename__ = "taxon_genus"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(12), nullable=False, unique=True)
    family_id = Column(Integer, ForeignKey(TaxonFamily.id), nullable=False)

    species: List["TaxonSpecies"] = relationship("TaxonSpecies", backref="genus")


class TaxonSpecies(Base):
    __tablename__ = "taxon_species"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(12), nullable=False, unique=True)
    genus_id = Column(Integer, ForeignKey(TaxonGenus.id), nullable=False)

    protection_class = Column(Enum(ProtectionClass))
    conservation_status = Column(Enum(ConservationStatus))
