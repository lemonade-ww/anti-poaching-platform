import datetime

from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session

from api.db.models import Defendant, Judgment
from api.db.utils import QueryFilter, apply_filters, optional_filters
from api.lib.errors import check_not_none
from api.lib.schemas import DefendantFilter


def from_defendant_filter(
    defendant_filter: DefendantFilter, judgment_id: int | None = None
) -> list[QueryFilter]:
    """Convert a filter object to a QueryFilter

    Args:
        defendant_filter (DefendantFilter): The filter object to be converted

    Returns:
        list[QueryFilter]: A list of query filters
    """
    return optional_filters(
        (Defendant.name, "in", defendant_filter.name),
        (Defendant.gender, "in", defendant_filter.gender),
        (Defendant.birth, ">", defendant_filter.birth_after),
        (Defendant.birth, "<", defendant_filter.birth_before),
        (Defendant.education_level, "in", defendant_filter.education_level),
        (Defendant.judgment_id, "=", judgment_id),
    )


def query_defendant(
    db: Session,
    defendant_filter: DefendantFilter,
    judgment_id: int | None = None,
) -> list[Defendant]:
    query = db.query(Defendant).options(joinedload(Defendant.judgment))
    result = apply_filters(
        query,
        from_defendant_filter(defendant_filter, judgment_id),
    ).all()
    return result


def insert_defendant(
    db: Session,
    judgment_id: int,
    name: str,
    gender: str = None,
    birth: datetime.date = None,
    education_level: str = None,
):
    judgment: Judgment = check_not_none(
        db.query(Judgment).filter(Judgment.id == judgment_id).first(),
        f"judgment {judgment_id}",
    )

    defendant = Defendant(
        name=name,
        birth=birth,
        gender=gender,
        education_level=education_level,
        judgment=judgment,
    )
    return defendant
