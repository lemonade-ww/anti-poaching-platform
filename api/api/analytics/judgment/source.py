from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from api.crud.source import insert_source, query_source
from api.dependencies import get_db
from api.lib import has_query_params
from api.lib.schemas import Source as SourceSchema
from api.lib.schemas import SourceFilter, SourcePost

router = APIRouter(prefix="/source")


@router.get("", response_model=list[SourceSchema])
def get_sources(
    source_filter: SourceFilter = Depends(has_query_params(SourceFilter)),
    db: Session = Depends(get_db),
):
    sources = query_source(db, source_filter)

    return sources


@router.post("/{judgment_id}", response_model=SourceSchema, status_code=201)
def post_source(judgment_id: int, source: SourcePost, db: Session = Depends(get_db)):
    new_source = insert_source(db, judgment_id, source)
    db.add(new_source)
    db.commit()

    return new_source
