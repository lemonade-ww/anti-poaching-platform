from fastapi.testclient import TestClient

from api.lib.errors import Reason, ResponseError, check_not_none
from api.main import app


@app.get("/test-errors")
def general_error_endpoint():
    raise ResponseError("Hola", Reason.ResourceDoesNotExist)


@app.get("/test-none-error")
def none_error_endpoint():
    def get_resource() -> str | None:
        d: dict = {}
        return d.get("something")

    _ = check_not_none(get_resource(), "customer asd")


def test_response_error(client: TestClient):
    result = client.get("/test-errors")

    assert result.json() == {
        "message": "Hola",
        "reason": Reason.ResourceDoesNotExist,
    }


def test_none_error(client: TestClient):
    result = client.get("/test-none-error")

    assert result.status_code == 400
    assert result.json()["reason"] == Reason.ResourceDoesNotExist
    assert "customer asd" in result.json()["message"]
