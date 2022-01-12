from api.lib import to_camel, to_snake


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