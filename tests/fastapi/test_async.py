import typing

import pytest
from starlette.testclient import TestClient

import strawberry
from tests.fastapi.app import create_app


@pytest.fixture
def test_client() -> TestClient:
    @strawberry.type
    class Query:
        @strawberry.field
        async def hello(self, name: typing.Optional[str] = None) -> str:
            return f"Hello {name or 'world'}"

    async_schema = strawberry.Schema(Query)
    app = create_app(schema=async_schema, example_query="Hello from Pytest")
    return TestClient(app)


def test_simple_query(test_client):
    response = test_client.post("/graphql", json={"query": "{ hello }"})

    assert response.json() == {"data": {"hello": "Hello world"}}


def test_example_query_is_updated(test_client):
    response = test_client.get("/graphql")
    assert 'React.useState("Hello from Pytest")' in response.text
