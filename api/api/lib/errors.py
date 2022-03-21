from typing import TypeVar

from fastapi import HTTPException

T = TypeVar("T")


class NoneException(HTTPException):
    def __init__(self, name: str, status_code: int = 422) -> None:
        super().__init__(
            status_code=status_code,
            detail=f"Resource does not exist: {name}",
        )


def check_not_none(to_check: T | None, name: str) -> T:
    """Check if `to_check` is `None`. Raise NoneException if it is None.
    This should only be used in a FastAPI path operation.

    Args:
        to_check (T | None): The Noneable variable to check
        name (str): The name of the missing resource that will be used in the error

    Raises:
        NoneException

    Returns:
        T: The original variable
    """
    if to_check is None:
        raise NoneException(name)
    return to_check
