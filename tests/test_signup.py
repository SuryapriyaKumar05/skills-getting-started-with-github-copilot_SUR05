"""
Tests for the POST /activities/{activity_name}/signup endpoint.

Uses Arrange-Act-Assert (AAA) pattern:
- Arrange: Set up test data and client
- Act: Make HTTP request with parameters
- Assert: Verify response status, payload, and side effects
"""

import pytest


class TestSignupForActivity:
    """Test suite for the POST signup endpoint."""
    
    def test_signup_for_existing_activity_returns_success(self, client):
        """
        Arrange: Valid activity name and email
        Act: POST /activities/Chess Club/signup?email=test@example.com
        Assert: Status code is 200 and response confirms signup
        """
        # Arrange
        activity_name = "Chess Club"
        email = "test@example.com"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
    
    def test_signup_response_contains_confirmation_message(self, client):
        """
        Arrange: Valid activity name and email
        Act: POST /activities/Chess Club/signup?email=test@example.com
        Assert: Response message confirms the signup details
        """
        # Arrange
        activity_name = "Chess Club"
        email = "test@example.com"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
    
    def test_signup_adds_email_to_participants(self, client):
        """
        Arrange: Valid activity name and email, baseline participant count
        Act: POST /activities/Programming Class/signup?email=newstudent@example.com
        Assert: Verify email was added to the activity's participant list
        """
        # Arrange
        activity_name = "Programming Class"
        email = "newstudent@example.com"
        
        # Get baseline participants
        baseline_response = client.get("/activities")
        baseline_participants = baseline_response.json()[activity_name]["participants"]
        
        # Act
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Verify side effect by fetching activities again
        updated_response = client.get("/activities")
        updated_participants = updated_response.json()[activity_name]["participants"]
        
        # Assert
        assert signup_response.status_code == 200
        assert len(updated_participants) == len(baseline_participants) + 1
        assert email in updated_participants
    
    def test_signup_for_nonexistent_activity_returns_404(self, client):
        """
        Arrange: Activity that doesn't exist
        Act: POST /activities/Nonexistent Activity/signup?email=test@example.com
        Assert: Status code is 404 and error detail is provided
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@example.com"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
    
    def test_signup_for_nonexistent_activity_includes_error_detail(self, client):
        """
        Arrange: Activity that doesn't exist
        Act: POST /activities/Nonexistent Activity/signup?email=test@example.com
        Assert: Error response includes "Activity not found" detail
        """
        # Arrange
        activity_name = "Unknown Class"
        email = "test@example.com"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "detail" in data
        assert "Activity not found" in data["detail"]
    
    def test_signup_does_not_modify_other_activities(self, client):
        """
        Arrange: Two different activities with baseline participant counts
        Act: Sign up for Chess Club only
        Assert: Other activities (Programming Class) remain unchanged
        """
        # Arrange
        signup_activity = "Chess Club"
        other_activity = "Programming Class"
        email = "another@example.com"
        
        # Get baseline state
        baseline_response = client.get("/activities")
        other_baseline = baseline_response.json()[other_activity]["participants"].copy()
        
        # Act
        client.post(
            f"/activities/{signup_activity}/signup",
            params={"email": email}
        )
        
        # Verify other activities unchanged
        updated_response = client.get("/activities")
        other_updated = updated_response.json()[other_activity]["participants"]
        
        # Assert
        assert other_updated == other_baseline
