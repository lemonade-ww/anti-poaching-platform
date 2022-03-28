from typing import Callable, TypeVar

T = TypeVar("T")


def unpack(
    f: Callable[..., T],
    data: dict[str, object],
    **kwargs: Callable[[], object],
) -> T:
    data = data.copy()
    # The overriden value will only be applied if the given key ALREADY exists
    # in the dictionary, thereby it is guaranteed that this key is available
    # if you recursively call unpack in one of the kwargs
    applied = {k: v() for k, v in kwargs.items() if k in data}
    # Combine the overriden value with the modified data dictionary
    data.update(applied)
    return f(**data)


def unpack_list(f: Callable[..., T], data: list[dict[str, object]]) -> list[T]:
    return [f(**item) for item in data]


def apply_non_none(f: Callable[..., T], *args: object, **kwargs: object) -> T:
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    return f(*args, **kwargs)
