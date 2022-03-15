import datetime
from typing import Any, Container, Iterable, Literal, TypeAlias

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine.result import Result
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import and_, or_
from sqlalchemy.sql.schema import Column

from api.db.models import ModelT

QueryFilter: TypeAlias = Any


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


def apply_filters(
    query: Query, filters: list[QueryFilter], use_or: bool = False
) -> Query:
    if len(filters) == 0:
        return query
    if use_or:
        return query.filter(or_(*filters))
    else:
        return query.filter(and_(*filters))


def optional_filters(
    *filters: tuple[
        Column,
        Literal["=", "~", "<", ">"],
        str | int | datetime.datetime | Column | None,
    ]
    | tuple[Column, Literal["in"], Container | None],
) -> list[QueryFilter]:
    """Generate a series of optional filters to the query

    Args:
        filters: A dict with the columns to be filtered as the key,
        a tuple of (filter operation, the value to be matched).
        Possible operations are:

        - = exact match
        - ~ contains
        - > greater than
        - < smaller than

    Returns:
        A list of column elements that can be applied to `query.filter`
    """
    result = []
    for key, operation, value in filters:
        if value is not None:
            if operation == "=":
                result.append(key == value)
            elif operation == "~":
                if isinstance(value, Column):
                    raise NotImplementedError("ilike between columns is not supported")
                result.append(key.ilike(f"%{value}%"))
            elif operation == ">":
                result.append(key > value)
            elif operation == "<":
                result.append(key < value)
            elif operation == "in":
                result.append(key.in_(value))
    return result
