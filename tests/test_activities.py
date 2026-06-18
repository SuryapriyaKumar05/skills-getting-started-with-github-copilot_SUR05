"""
Tests for the GET /activities endpoint.

Uses Arrange-Act-Assert (AAA) pattern:
- Arrange: Set up test data and client
- Act: Make HTTP request
- Assert: Verify response status, structure, and content
"""

import pytest


class TestGetActivities:
    """Test suite for the GET /activities endpoint."""
    
    def test_get_activities_returns_success_status(self, client):
        """
        Arrange: TestClient is ready
        Act: GET /activities
        Assert: Status code is 200
        """
        # Arrange
        # client fixture already initialized
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
    
    def test_get_activities_returns_dict_response(self, client):
        """
        Arrange: TestClient is ready
        Act: GET /activities
        Assert: Response body is a dictionary (JSON object)
        """
        # Arrange
        # client fixture already initialized
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert isinstance(data, dict)
    
    def test_get_activities_includes_expected_activities(self, client):
        """
        Arrange: TestClient is ready
        Act: GET /activities
        Assert: Response includes all three expected activities
        """
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name in expected_activities:
            assert activity_name in data
    
    def test_get_activities_includes_required_fields(self, client):
        """
        Arrange: TestClient is ready
        Act: GET /activities
        Assert: Each activity has required fields (description, schedule, max_participants, participants)
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            for field in required_fields:
                assert field in activity_data, f"Activity '{activity_name}' missing field '{field}'"
    
    def test_get_activities_participants_is_list(self, client):
        """
        Arrange: TestClient is ready
        Act: GET /activities
        Assert: Participants field for each activity is a list
        """
        # Arrange
        # client fixture already initialized
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list), \
                f"Participants for '{activity_name}' is not a list"
    
    def test_get_activities_includes_initial_participants(self, client):
        """
        Arrange: TestClient is ready with predefined participants
        Act: GET /activities
        Assert: Response includes pre-populated participant email addresses
        """
        # Arrange
        expected_participants = {
            "Chess Club": ["michael@mergington.edu", "daniel@mergington.edu"],
            "Programming Class": ["emma@mergington.edu", "sophia@mergington.edu"],
            "Gym Class": ["john@mergington.edu", "olivia@mergington.edu"]
        }
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, participants in expected_participants.items():
            assert data[activity_name]["participants"] == participants
