from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session

from api.db.models import Judgment, TaxonSpecies
from api.db.utils import optional_filters


def query_judgment(db: Session, title: str | None) -> list[Judgment]:
    query = db.query(Judgment).options(joinedload(Judgment.species))
    result = optional_filters(query, (Judgment.title, "~", title)).all()
    return result


def insert_judgment(db: Session, title: str, species_names: list[str]) -> Judgment:
    species: list[TaxonSpecies] = (
        db.query(TaxonSpecies).filter(TaxonSpecies.name.in_(species_names)).all()
    )
    judgment = Judgment(title=title, species=species)

    return judgment
