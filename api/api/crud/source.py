from sqlalchemy.orm.session import Session

from api.db.models import Defendant, Judgment, Source
from api.db.utils import QueryFilter, apply_filters, optional_filters
from api.lib.errors import check_not_none
from api.lib.schemas import SourceFilter, SourcePost


def from_source_filter(source_filter: SourceFilter) -> list[QueryFilter]:
    """Convert a filter object to a QueryFilter

    Args:
        source_filter (SourceFilter): The filter object to be converted

    Returns:
        list[QueryFilter]: A list of query filters
    """
    return optional_filters(
        (Source.judgment_id, "=", source_filter.judgment_id),
        (Source.defendant_id, "=", source_filter.defendant_id),
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


def insert_source(db: Session, judgment_id: int, data: SourcePost) -> Source:
    judgment: Judgment = check_not_none(
        db.query(Judgment).filter(Judgment.id == judgment_id).first(),
        f"judgment {judgment_id}",
    )

    defendant: Defendant | None = None

    if data.defendant_id is not None:
        defendant = check_not_none(
            db.query(Defendant).filter(Defendant.id == data.defendant_id).first(),
            f"defendant {data.defendant_id}",
        )

    source = Source(
        category=data.category,
        seller=data.seller,
        buyer=data.buyer,
        occasion=data.occasion,
        destination=data.destination,
        method=data.method,
        usage=data.usage,
        judgment=judgment,
        defendant=defendant,
    )
    return source
