import pytest
from fastapi.testclient import TestClient

from copilot_integration_example.api import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
