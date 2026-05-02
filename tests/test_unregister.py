"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint.

This module tests student unregistration functionality for extracurricular activities.
"""

import pytest


class TestUnregister:
    """Test suite for DELETE /activities/{activity_name}/unregister endpoint."""
    
    def test_unregister_successful_returns_200(self, client):
        """Test that a successful unregister returns a 200 status code."""
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 200
    
    def test_unregister_successful_returns_message(self, client):
        """Test that a successful unregister returns a success message."""
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]
        assert "michael@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]
    
    def test_unregister_removes_participant_from_activity(self, client):
        """Test that unregister actually removes the participant from the activity."""
        email = "michael@mergington.edu"
        
        # Verify participant is before unregister
        before = client.get("/activities").json()
        assert email in before["Chess Club"]["participants"]
        
        # Unregister
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify participant is removed
        after = client.get("/activities").json()
        assert email not in after["Chess Club"]["participants"]
    
    def test_unregister_nonexistent_activity_returns_404(self, client):
        """Test that unregistering from a non-existent activity returns 404."""
        response = client.delete(
            "/activities/Nonexistent Activity/unregister",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_unregister_student_not_in_activity_returns_400(self, client):
        """Test that unregistering a student not in the activity returns 400."""
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "notstudent@mergington.edu"}
        )
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]
    
    def test_unregister_missing_email_parameter_returns_422(self, client):
        """Test that unregistering without email parameter returns 422 (validation error)."""
        response = client.delete("/activities/Chess Club/unregister")
        assert response.status_code == 422
    
    def test_unregister_maintains_other_participants(self, client):
        """Test that unregistering one student doesn't remove others."""
        email_to_remove = "michael@mergington.edu"
        email_to_keep = "daniel@mergington.edu"
        
        # Get original participants
        before = client.get("/activities").json()
        original_participants = before["Chess Club"]["participants"].copy()
        
        # Unregister one student
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": email_to_remove}
        )
        assert response.status_code == 200
        
        # Get updated list
        after = client.get("/activities").json()
        new_participants = after["Chess Club"]["participants"]
        
        # Removed email should not be present
        assert email_to_remove not in new_participants
        # Other email should still be present
        assert email_to_keep in new_participants
    
    def test_unregister_twice_second_attempt_returns_400(self, client):
        """Test that unregistering the same student twice fails on second attempt."""
        email = "michael@mergington.edu"
        
        # First unregister should succeed
        response1 = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Second unregister should fail (student no longer registered)
        response2 = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert response2.status_code == 400
        assert "not signed up" in response2.json()["detail"]
    
    def test_unregister_from_each_activity_type(self, client):
        """Test that students can unregister from different activity types."""
        activities_with_participants = {
            "Chess Club": "michael@mergington.edu",
            "Programming Class": "emma@mergington.edu",
            "Gym Class": "john@mergington.edu",
            "Basketball Team": "alex@mergington.edu",
            "Soccer Club": "liam@mergington.edu",
            "Art Club": "isabella@mergington.edu",
            "Drama Club": "mason@mergington.edu",
            "Debate Club": "ethan@mergington.edu",
            "Science Club": "harper@mergington.edu"
        }
        
        for activity, email in activities_with_participants.items():
            response = client.delete(
                f"/activities/{activity}/unregister",
                params={"email": email}
            )
            assert response.status_code == 200, f"Failed to unregister from {activity}"
            
            # Verify removal
            after = client.get("/activities").json()
            assert email not in after[activity]["participants"]
    
    def test_unregister_case_sensitive_activity_name(self, client):
        """Test that activity names are case-sensitive for unregister."""
        # "chess club" (lowercase) should not match "Chess Club"
        response = client.delete(
            "/activities/chess club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 404
    
    def test_signup_then_unregister_workflow(self, client):
        """Test the complete workflow: signup then unregister."""
        email = "workflow@mergington.edu"
        activity = "Chess Club"
        
        # Initially not signed up
        before = client.get("/activities").json()
        assert email not in before[activity]["participants"]
        
        # Sign up
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200
        
        # Verify signed up
        middle = client.get("/activities").json()
        assert email in middle[activity]["participants"]
        
        # Unregister
        unregister_response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        assert unregister_response.status_code == 200
        
        # Verify unregistered
        after = client.get("/activities").json()
        assert email not in after[activity]["participants"]
