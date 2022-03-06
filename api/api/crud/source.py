from sqlalchemy.orm.session import Session

from api.db.models import Source
from api.db.utils import optional_filters
from api.lib.schemas import Source as SourceSchema
from api.lib.schemas import SourceFilter


def query_source(db: Session, source_filter: SourceFilter) -> list[Source]:
    query = db.query(Source)
    result = optional_filters(
        query,
        (Source.judgment_id, "=", source_filter.judgment_id),
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
        judgment_id=data.judgment_id,
    )
    db.add(source)

    return source
