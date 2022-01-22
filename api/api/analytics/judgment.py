from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm.session import Session

from api.crud.judgment import insert_judgment, query_judgment
from api.dependencies import get_db
from api.lib import APIModel
from api.lib.schemas import ActionResult
from api.lib.schemas import Judgment as JudgmentSchema
from api.lib.schemas import QueryActionResult, ResponseStatus

router = APIRouter(prefix="/analytics/judgment")


class JudgmentFilter(APIModel):
    title: str | None


class JudgmentPost(APIModel):
    title: str
    species_names: list[str]


@router.get("", response_model=QueryActionResult[list[JudgmentSchema]])
def get_judgment(
    judgment_filter: JudgmentFilter = Depends(), db: Session = Depends(get_db)
):
    result = query_judgment(db, judgment_filter.title)
    return QueryActionResult(
        status=ResponseStatus.Success,
        result=result,
    )


@router.post("", response_model=ActionResult)
def post_judgment(judgment: JudgmentPost, db: Session = Depends(get_db)):
    insert_judgment(
        db,
        title=judgment.title,
        species_names=judgment.species_names,
    )
    db.commit()
    return ActionResult(
        status=ResponseStatus.Success,
    )
