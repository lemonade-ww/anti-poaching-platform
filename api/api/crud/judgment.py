from sqlalchemy.orm.session import Session

from api.db.models import Judgment, TaxonSpecies
from api.db.utils import QueryFilter, apply_filters, optional_filters
from api.lib.schemas import JudgmentFilter

def from_judgment_filter(judgment_filter: JudgmentFilter) -> list[QueryFilter]:
    """Convert a filter object to a QueryFilter

    Args:
        f (SpeciesFilter): The filter object to be converted

    Returns:
        list[QueryFilter]: A list of query filters
    """
    return optional_filters(
        (Judgment.id, "=", judgment_filter.judgment_id),
        (Judgment.title, "~", judgment_filter.title),
        (Judgment.location, "in", judgment_filter.locations),
        (Judgment.date_released, "<", judgment_filter.date_before),
        (Judgment.date_released, ">", judgment_filter.date_after),
    )


def query_judgment(db: Session, judgment_filter: JudgmentFilter) -> list[Judgment]:
    # Process the filters that do not require joining first
    query = db.query(Judgment)
    apply_filters(query, from_judgment_filter(judgment_filter))

    return query.all()


def insert_judgment(db: Session, title: str, species_names: list[str]) -> Judgment:
    species: list[TaxonSpecies] = (
        db.query(TaxonSpecies).filter(TaxonSpecies.name.in_(species_names)).all()
    )
    judgment = Judgment(title=title, species=species)
    return judgment
