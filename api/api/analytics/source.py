from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from api.crud.source import insert_source, query_source
from api.dependencies import get_db
from api.lib.schemas import APIModel, QueryActionResult
from api.lib.schemas import Source as SourceSchema
from api.lib.schemas import SourceCategory


class SourceFilter(APIModel):
    judgment_id: int
    category: SourceCategory
    occasion: str
    seller: str
    buyer: str | None
    method: str | None
    destination: str | None
    usage: str | None


SourcePost = SourceSchema

router = APIRouter(prefix="/analytics/sources")


@router.get("", response_model=QueryActionResult[list[SourceSchema]])
def get_source(source_filter: SourceFilter = Depends(), db: Session = Depends(get_db)):
    sources = query_source(db, source_filter)
    return QueryActionResult(result=sources)

@router.post("", response_model=QueryActionResult[SourceSchema])
def post_source(source: SourcePost = Depends(), db: Session = Depends(get_db)):
    source = insert_source(db, source)
    db.flush()

    return QueryActionResult(result=SourceSchema(
        judgment_id=source.judgment_id,
        category=source.category,
        occasion=source.occasion,
        seller=source.seller,
        buyer=source.buyer,
        method=source.method,
        destination=source.destination,
        usage=source.usage,
    ))
