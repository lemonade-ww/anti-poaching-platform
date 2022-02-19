from enum import Enum
from typing import TypeVar

from fastapi import Request
from fastapi.responses import JSONResponse

T = TypeVar("T")


class Reason(str, Enum):
    ResourceDoesNotExist = "resource_does_not_exist"


class ResponseError(Exception):
    status_code: int = 400

    def __init__(self, msg: str, reason: Reason) -> None:
        self.msg = msg
        self.reason = reason


class NoneError(ResponseError):
    def __init__(self, name: str) -> None:
        super().__init__(
            f"Resource does not exist: {name}",
            reason=Reason.ResourceDoesNotExist,
        )


def response_error_handler(request: Request, exc: ResponseError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.msg,
            "reason": exc.reason,
        },
    )


def check_not_none(to_check: T | None, name: str) -> T:
    if to_check is None:
        raise NoneError(name)
    return to_check
