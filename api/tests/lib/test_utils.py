from fastapi.dependencies.utils import get_typed_signature

from api.lib import APIModel, has_query_params, to_camel, to_snake


def test_to_snake():
    assert to_snake("Class") == "class"
    assert to_snake("TestCase") == "test_case"
    assert to_snake("ABC") == "a_b_c"
    assert to_snake("_TestCase") == "test_case"
    assert to_snake("TestCase_") == "test_case_"


def test_to_camel():
    assert to_camel("test") == "test"
    assert to_camel("class_") == "class"
    assert to_camel("asd_asd_asd") == "asdAsdAsd"
    assert to_camel("_asasd") == "asasd"
    assert to_camel("wa__kwasd") == "waKwasd"


def test_has_query_params():
    class TestModel(APIModel):
        regular: str
        str_list: list[str]
        str_list_allow_none: list[str] | None
        str_allow_none: str | None
        str_list_default: list[str] = ["test"]

    wrapped = has_query_params(TestModel)

    original_sig = get_typed_signature(TestModel)
    new_sig = get_typed_signature(wrapped)

    assert (
        repr(original_sig)
        == "<Signature (*, regular: str, strList: list[str], strListAllowNone: list[str] = None, strAllowNone: str = None, strListDefault: list[str] = ['test'])>"
    )
    assert (
        repr(new_sig)
        == "<Signature (*, regular: str = None, strList: list[str] = Query([]), strListAllowNone: list[str] = Query(None), strAllowNone: str = None, strListDefault: list[str] = Query(['test']))>"
    )
