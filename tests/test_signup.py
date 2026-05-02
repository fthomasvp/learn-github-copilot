"""
Tests for the POST /activities/{activity_name}/signup endpoint.

This module tests student signup functionality for extracurricular activities.
"""

import pytest


class TestSignup:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_successful_returns_200(self, client):
        """Test that a successful signup returns a 200 status code."""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
    
    def test_signup_successful_returns_message(self, client):
        """Test that a successful signup returns a success message."""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        data = response.json()
        assert "message" in data
        assert "Signed up" in data["message"]
        assert "newstudent@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]
    
    def test_signup_adds_participant_to_activity(self, client):
        """Test that signup actually adds the participant to the activity."""
        new_email = "newstudent@mergington.edu"
        
        # Signup
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": new_email}
        )
        assert response.status_code == 200
        
        # Verify participant is now in the list
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert new_email in activities["Chess Club"]["participants"]
    
    def test_signup_duplicate_email_returns_400(self, client):
        """Test that signing up with an email that's already registered returns 400."""
        # michael@mergington.edu is already in Chess Club
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_nonexistent_activity_returns_404(self, client):
        """Test that signing up for a non-existent activity returns 404."""
        response = client.post(
            "/activities/Nonexistent Activity/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_missing_email_parameter_returns_422(self, client):
        """Test that signing up without email parameter returns 422 (validation error)."""
        response = client.post("/activities/Chess Club/signup")
        assert response.status_code == 422
    
    def test_signup_multiple_students_same_activity(self, client):
        """Test that multiple different students can sign up for the same activity."""
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email1}
        )
        response2 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email2}
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify both are now in the list
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email1 in activities["Chess Club"]["participants"]
        assert email2 in activities["Chess Club"]["participants"]
    
    def test_signup_same_student_different_activities(self, client):
        """Test that the same student can sign up for multiple activities."""
        email = "newstudent@mergington.edu"
        
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        response2 = client.post(
            "/activities/Programming Class/signup",
            params={"email": email}
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify student is in both activities
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]
        assert email in activities["Programming Class"]["participants"]
    
    def test_signup_case_sensitive_activity_name(self, client):
        """Test that activity names are case-sensitive."""
        # "chess club" (lowercase) should not match "Chess Club"
        response = client.post(
            "/activities/chess club/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
    
    def test_signup_maintains_other_participants(self, client):
        """Test that signing up a new student doesn't remove existing participants."""
        new_email = "newstudent@mergington.edu"
        
        # Get original participants
        before = client.get("/activities").json()
        original_chess_participants = before["Chess Club"]["participants"].copy()
        
        # Sign up new student
        client.post(
            "/activities/Chess Club/signup",
            params={"email": new_email}
        )
        
        # Get updated participants
        after = client.get("/activities").json()
        new_chess_participants = after["Chess Club"]["participants"]
        
        # Original participants should still be there
        for original_email in original_chess_participants:
            assert original_email in new_chess_participants
    
    def test_signup_to_each_activity_type(self, client):
        """Test that students can sign up for different activity types."""
        email = "multiactivity@mergington.edu"
        activities_to_test = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Soccer Club",
            "Art Club",
            "Drama Club",
            "Debate Club",
            "Science Club"
        ]
        
        for activity in activities_to_test:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200, f"Failed to signup for {activity}"
