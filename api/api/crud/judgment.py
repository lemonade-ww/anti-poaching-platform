from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session

from api.crud.defendant import from_defendant_filter
from api.crud.source import from_source_filter
from api.crud.species import from_species_filter
from api.db.models import Judgment, TaxonSpecies
from api.db.utils import QueryFilter, apply_filters, optional_filters
from api.lib.schemas import JudgmentFilter


def from_judgment_filter(judgment_filter: JudgmentFilter) -> list[QueryFilter]:
    """Convert a filter object to a QueryFilter

    Args:
        judgment_filter (JudgmentFilter): The filter object to be converted

    Returns:
        list[QueryFilter]: A list of query filters
    """
    return optional_filters(
        (Judgment.id, "=", judgment_filter.judgment_id),
        (Judgment.title, "~", judgment_filter.title),
        (Judgment.location, "in", judgment_filter.location),
        (Judgment.date_released, "<", judgment_filter.date_before),
        (Judgment.date_released, ">", judgment_filter.date_after),
    )


def query_judgment(
    db: Session,
    judgment_filter: JudgmentFilter,
) -> list[Judgment]:
    print(judgment_filter.json())
    # Process the filters that do not require joining first
    query = db.query(Judgment)
    query = apply_filters(query, from_judgment_filter(judgment_filter))

    # There are three sub-filters to consider: species filter, defendant
    # filter, and sources filter. We handle them separately
    species_query_filters = from_species_filter(judgment_filter.species_filter)
    if len(species_query_filters) > 0:
        # Only join the relationship and apply the filter if there is any
        query = query.join(Judgment.species)
        query = apply_filters(query, species_query_filters)

    defendant_query_filters = from_defendant_filter(judgment_filter.defendant_filter)
    if len(defendant_query_filters) > 0:
        query = query.join(Judgment.defendants)
        query = apply_filters(query, defendant_query_filters)

    source_query_filters = from_source_filter(judgment_filter.source_filter)
    if len(source_query_filters) > 0:
        query = query.join(Judgment.sources)
        query = apply_filters(query, source_query_filters)

    res = query.all()
    return res


def insert_judgment(db: Session, title: str, species_names: list[str]) -> Judgment:
    species: list[TaxonSpecies] = (
        db.query(TaxonSpecies).filter(TaxonSpecies.name.in_(species_names)).all()
    )
    judgment = Judgment(title=title, species=species)
    return judgment
