from sqlalchemy.orm.session import Session

from api.analytics.source import SourceFilter
from api.db.models import Source
from api.db.utils import optional_filters
from api.lib.schemas import Source as SourceSchema


def query_source(db: Session, source_filter: SourceFilter) -> list[Source]:
    query = db.query(Source)
    result = optional_filters(
        query,
        (Source.category, "=", source_filter.category),
        (Source.seller, "~", source_filter.seller),
        (Source.buyer, "~", source_filter.buyer),
        (Source.occasion, "~", source_filter.occasion),
        (Source.destination, "~", source_filter.destination),
        (Source.method, "~", source_filter.method),
        (Source.usage, "~", source_filter.usage),
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
    )
    db.add(source)

    return source
