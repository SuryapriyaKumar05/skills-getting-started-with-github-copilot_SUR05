"""
Shared test fixtures for FastAPI backend tests.

Provides:
- TestClient for making HTTP requests to the FastAPI app
- Activity state reset to ensure test isolation
"""

import pytest
from fastapi.testclient import TestClient
import copy
from src.app import app, activities

# Store the original activity state for resetting between tests
ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture
def client():
    """
    Provide a TestClient for the FastAPI application.
    
    Resets the in-memory activities state before each test to ensure
    isolation and deterministic behavior.
    """
    # Arrange: Reset activities to known state before each test
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    
    return TestClient(app)
