import datetime
from typing import Any, Iterable, Literal

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine.result import Result
from sqlalchemy.orm.query import Query
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


def optional_filters(
    query: Query,
    *filters: tuple[
        Column,
        Literal["=", "~", "<", ">", "in"],
        str | int | datetime.datetime | Column | None,
    ],
) -> Query:
    """Generate a series of optional filters to the query

    Args:
        query (Query): The query to be modified
        filters: A dict with the columns to be filtered as the key,
        a tuple of (filter operation, the value to be matched).
        Possible operations are:

        - = exact match
        - ~ contains
        - > greater than
        - < smaller than

    Returns:
        Query: [description]
    """
    for key, operation, value in filters:
        if value is not None:
            if operation == "=":
                query = query.filter(key == value)
            elif operation == "~":
                if isinstance(value, Column):
                    raise NotImplementedError("ilike between columns is not supported")
                query = query.filter(key.ilike(f"%{value}%"))
            elif operation == ">":
                query = query.filter(key > value)
            elif operation == "<":
                query = query.filter(key < value)
            elif operation == "in":
                query = query.filter(key.in_(value))
    return query
