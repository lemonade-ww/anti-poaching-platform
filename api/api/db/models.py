from typing import List, Type, TypeVar

from sqlalchemy import Enum, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.decl_api import declared_attr
from sqlalchemy.sql.schema import Column, ForeignKey

from api.lib import to_snake
from api.lib.schemas import ConservationStatus, ProtectionClass


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

    orders: List["TaxonOrder"] = relationship("TaxonOrder", backref="class_")


class TaxonOrder(Base, IdMixin):
    name = Column(String(255), nullable=False, unique=True)
    class_id = Column(Integer, ForeignKey(TaxonClass.id), nullable=False)

    families: List["TaxonFamily"] = relationship("TaxonFamily", backref="order")


class TaxonFamily(Base, IdMixin):
    name = Column(String(255), nullable=False, unique=True)
    order_id = Column(Integer, ForeignKey(TaxonOrder.id), nullable=False)

    genuses: List["TaxonGenus"] = relationship("TaxonGenus", backref="family")


class TaxonGenus(Base, IdMixin):
    name = Column(String(255), nullable=False, unique=True)
    family_id = Column(Integer, ForeignKey(TaxonFamily.id), nullable=False)

    species: List["TaxonSpecies"] = relationship("TaxonSpecies", backref="genus")


class TaxonSpecies(Base, IdMixin):
    name = Column(String(255), nullable=False, unique=True)
    genus_id = Column(Integer, ForeignKey(TaxonGenus.id), nullable=False)

    protection_class = Column(Enum(ProtectionClass))
    conservation_status = Column(Enum(ConservationStatus))
