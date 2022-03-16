from fastapi import APIRouter, Depends
from pydantic import parse_obj_as
from sqlalchemy.orm.session import Session

from api.crud.source import insert_source, query_source
from api.dependencies import get_db
from api.lib.schemas import QueryActionResult, ResponseStatus
from api.lib.schemas import Source as SourceSchema
from api.lib.schemas import SourceFilter, SourcePost

router = APIRouter(prefix="/analytics/source")


@router.get("", response_model=QueryActionResult[list[SourceSchema]])
def get_source(source_filter: SourceFilter = Depends(), db: Session = Depends(get_db)):
    sources = query_source(db, source_filter)
    return QueryActionResult(
        status=ResponseStatus.Success,
        result=parse_obj_as(list[SourceSchema], sources),
    )


@router.post("", response_model=QueryActionResult[SourceSchema])
def post_source(source: SourcePost, db: Session = Depends(get_db)):
    new_source = insert_source(db, source)
    db.add(new_source)
    db.commit()

    return QueryActionResult(
        status=ResponseStatus.Success,
        result=SourceSchema.from_orm(new_source),
    )
