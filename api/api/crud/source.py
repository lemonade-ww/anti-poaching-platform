from sqlalchemy.orm.session import Session

from api.db.models import Source
from api.db.utils import QueryFilter, apply_filters, optional_filters
from api.lib.schemas import Source as SourceSchema
from api.lib.schemas import SourceFilter


def from_source_filter(source_filter: SourceFilter) -> list[QueryFilter]:
    """Convert a filter object to a QueryFilter

    Args:
        source_filter (SourceFilter): The filter object to be converted

    Returns:
        list[QueryFilter]: A list of query filters
    """
    return optional_filters(
        (Source.judgment_id, "=", source_filter.judgment_id),
        (Source.category, "in", source_filter.category),
        (Source.seller, "in", source_filter.seller),
        (Source.buyer, "in", source_filter.buyer),
        (Source.occasion, "in", source_filter.occasion),
        (Source.destination, "in", source_filter.destination),
        (Source.method, "in", source_filter.method),
        (Source.usage, "in", source_filter.usage),
    )


def query_source(db: Session, source_filter: SourceFilter) -> list[Source]:
    query = db.query(Source)
    result = apply_filters(
        query,
        from_source_filter(source_filter),
    ).all()
    return result


def insert_source(db: Session, data: SourceSchema) -> Source:
    source = Source(
        category=data.category,
        seller=data.seller,
        buyer=data.buyer,
        occasion=data.occasion,
        destination=data.destination,
        method=data.method,
        usage=data.usage,
        judgment_id=data.judgment_id,
    )
    return source
