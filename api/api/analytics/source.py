from fastapi import APIRouter, Depends
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
        result=sources,
    )


@router.post("", response_model=QueryActionResult[SourceSchema])
def post_source(source: SourcePost, db: Session = Depends(get_db)):
    new_source = insert_source(db, source)
    db.add(new_source)
    db.commit()

    return QueryActionResult(
        status=ResponseStatus.Success,
        result=SourceSchema(
            judgment_id=new_source.judgment_id,
            category=new_source.category,
            occasion=new_source.occasion,
            seller=new_source.seller,
            buyer=new_source.buyer,
            method=new_source.method,
            destination=new_source.destination,
            usage=new_source.usage,
        ),
    )
