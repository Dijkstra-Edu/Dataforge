"""
Shared pytest fixtures. App is imported with pythonpath=app (see pytest.ini).
"""
import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client() -> TestClient:
    """FastAPI TestClient for the main app."""
    return TestClient(app)
