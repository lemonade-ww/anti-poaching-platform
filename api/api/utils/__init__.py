from typing import Any, Iterable, OrderedDict, TypeVar
from weakref import WeakValueDictionary

from pydantic.main import BaseModel

T = TypeVar("T")


def to_camel(string: str) -> str:
    string.removesuffix("_")
    words = [word for word in string.split("_") if len(word) > 0]
    return "".join(word.capitalize() if i > 0 else word for i, word in enumerate(words))


class APIModel(BaseModel):
    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


def get_unique_attributes(
    objs: Iterable[T], attributes: Iterable[str]
) -> OrderedDict[str, tuple[set[Any], WeakValueDictionary[Any, T]]]:
    """Find the unique attributes of a list of given object

    Args:
        objs (Iterable[T]): The objects to be processed
        attributes (Iterable[str]): The attributes to be looked up

    Returns:
        tuple[OrderedDict[str, tuple[set[Any], WeakValueDictionary[Any, T]]]]: \
            An ordered dictionary containing: \
                a unique set for each of the attributes preserving the order of the attributes; \
                and a WeakValueDictionary containing a mapping from the value of the attributes \
                    to the original objects.
    """
    result = OrderedDict()
    for attribute in attributes:
        ref: WeakValueDictionary[Any, T] = WeakValueDictionary()
        unique_set = set()
        for obj in objs:
            val = getattr(obj, attribute)
            ref[val] = obj
            unique_set.add(val)
        result[attribute] = (unique_set, ref)
    return result


def map_attribute(
    objects: Iterable[object], source_key: str, value_key: str
) -> dict[str, Any]:
    """Map one attribute to another for a list of objects

    Args:
        objects (Iterable[object]): The objects to be mapped
        source_key (str): The key of the attribute that will be mapped FROM
        value_key (str): The key of the attribute that will be mapped TO

    Returns:
        dict[str, Any]: The mapped dictionary
    """
    return {getattr(obj, source_key): getattr(obj, value_key) for obj in objects}
