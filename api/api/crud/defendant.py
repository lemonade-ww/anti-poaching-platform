import datetime

from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session

from api.db.models import Defendant, Judgment
from api.db.utils import optional_filters
from api.lib.errors import check_not_none


def query_defendant(
    db: Session,
    judgment_id: int = None,
    name: str = None,
    gender: str = None,
    birth_before: datetime.datetime = None,
    birth_after: datetime.datetime = None,
    education_level: str = None,
) -> list[Defendant]:
    query = db.query(Defendant).options(joinedload(Defendant.judgment))
    result = optional_filters(
        query,
        (Defendant.name, "~", name),
        (Defendant.gender, "=", gender),
        (Defendant.birth, ">", birth_after),
        (Defendant.birth, "<", birth_before),
        (Defendant.education_level, "=", education_level),
        (Defendant.judgment_id, "=", judgment_id),
    ).all()
    return result


def insert_defendant(
    db: Session,
    judgment_id: int,
    name: str,
    gender: str = None,
    birth: datetime.datetime = None,
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
