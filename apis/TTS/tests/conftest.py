from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient for each test case.
    """
    with TestClient(app) as client:
        yield client
