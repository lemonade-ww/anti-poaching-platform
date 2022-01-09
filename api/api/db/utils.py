from typing import Any, Iterable

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine.result import Result
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import Column

from api.db.models import ModelT


def bulk_upsert(
    db: Session,
    Model: ModelT,
    *returning: Column,
    values: Iterable[dict[str, Any]],
    update_keys: Iterable[str],
    index_elements: Iterable[str | Column],
) -> Result:
    """Upsert rows in bulk with returning values

    Args:
        Model (ModelT): The table to upsert
        values (Iterable[dict[str, Any]]): The key-values in a list of dictionary format
        update_keys (Iterable[str]): The keys to be updated when a conflict occurs
        index_elements (Iterable[str | Column]): The index elements for the columns

    Returns:
        List[dict[str, Any]]: The list of returning data
    """
    insert_stmt = insert(Model).values(values)
    upsert_stmt = insert_stmt.returning(*returning).on_conflict_do_update(
        index_elements=index_elements,
        set_={key: getattr(insert_stmt.excluded, key) for key in update_keys},
    )
    result = db.execute(upsert_stmt)
    db.flush()
    return result
