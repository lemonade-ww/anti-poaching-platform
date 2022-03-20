from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from pydantic import parse_obj_as
from sqlalchemy.orm.session import Session

from api.crud.defendant import insert_defendant
from api.crud.judgment import insert_judgment, query_judgment
from api.dependencies import get_db
from api.lib import has_query_params
from api.lib.schemas import ActionResult
from api.lib.schemas import Judgment as JudgmentSchema
from api.lib.schemas import (
    JudgmentFilter,
    JudgmentPost,
    QueryActionResult,
    ResponseStatus,
)

router = APIRouter(prefix="/analytics/judgment")


@router.get("", response_model=QueryActionResult[list[JudgmentSchema]])
def search_judgments(
    judgment_filter: JudgmentFilter = Depends(has_query_params(JudgmentFilter)),
    db: Session = Depends(get_db),
):
    result = query_judgment(db, judgment_filter)
    return QueryActionResult(
        status=ResponseStatus.Success,
        result=parse_obj_as(list[JudgmentSchema], result),
    )


@router.get("/{id}", response_model=QueryActionResult[JudgmentSchema])
def get_judgment(id: int, db: Session = Depends(get_db)):
    result = query_judgment(
        db, judgment_filter=JudgmentFilter.no_depends(judgment_id=id)
    )

    if len(result) == 0:
        raise HTTPException(status_code=404, detail=f"Judgment does not exist")
    else:
        return QueryActionResult(
            status=ResponseStatus.Success,
            result=parse_obj_as(JudgmentSchema, result[0]),
        )


@router.post("", response_model=ActionResult)
def post_judgment(judgment: JudgmentPost, db: Session = Depends(get_db)):
    # Insert the judgment first
    # Flush but do not commit
    judgment_inserted = insert_judgment(
        db,
        JudgmentPost(
            title=judgment.title,
            species_names=judgment.species_names,
        ),
    )
    db.add(judgment_inserted)
    db.flush()

    # Assuming that the insertion was successful
    assert judgment_inserted.id is not None

    # Insert the defendants in the requests for this judgment
    defendants_inserted = []

    # Loop through the defendants and insert them here
    for defendant in judgment.defendants:
        defendants_inserted.append(
            insert_defendant(
                db,
                judgment_id=judgment_inserted.id,
                name=defendant.name,
                gender=defendant.gender,
                birth=defendant.birth,
                education_level=defendant.education_level,
            )
        )

    db.add_all(defendants_inserted)
    db.commit()

    return ActionResult(
        status=ResponseStatus.Success,
    )
