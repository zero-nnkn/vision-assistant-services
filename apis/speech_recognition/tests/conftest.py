import os
import sys
from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 

from src.main import app

@pytest.fixture(scope="function")
def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient for each test case.
    """
    with TestClient(app) as client:
        yield client