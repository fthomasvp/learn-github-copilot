"""
Tests for the GET /activities endpoint.

This module tests retrieving all extracurricular activities and their details.
"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint."""
    
    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns a 200 status code."""
        response = client.get("/activities")
        assert response.status_code == 200
    
    def test_get_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary."""
        response = client.get("/activities")
        assert isinstance(response.json(), dict)
    
    def test_get_activities_returns_all_nine_activities(self, client):
        """Test that all 9 activities are returned."""
        response = client.get("/activities")
        activities = response.json()
        
        expected_activities = [
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
        
        assert len(activities) == 9
        for activity_name in expected_activities:
            assert activity_name in activities
    
    def test_get_activities_contains_required_fields(self, client):
        """Test that each activity has required fields."""
        response = client.get("/activities")
        activities = response.json()
        
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        for activity_name, activity_data in activities.items():
            for field in required_fields:
                assert field in activity_data, f"{activity_name} missing field: {field}"
    
    def test_get_activities_chess_club_correct_data(self, client):
        """Test that Chess Club has correct data."""
        response = client.get("/activities")
        activities = response.json()
        chess_club = activities["Chess Club"]
        
        assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
        assert chess_club["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
        assert chess_club["max_participants"] == 12
        assert chess_club["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]
    
    def test_get_activities_programming_class_correct_data(self, client):
        """Test that Programming Class has correct data."""
        response = client.get("/activities")
        activities = response.json()
        prog_class = activities["Programming Class"]
        
        assert prog_class["description"] == "Learn programming fundamentals and build software projects"
        assert prog_class["schedule"] == "Tuesdays and Thursdays, 3:30 PM - 4:30 PM"
        assert prog_class["max_participants"] == 20
        assert prog_class["participants"] == ["emma@mergington.edu", "sophia@mergington.edu"]
    
    def test_get_activities_gym_class_correct_data(self, client):
        """Test that Gym Class has correct data."""
        response = client.get("/activities")
        activities = response.json()
        gym_class = activities["Gym Class"]
        
        assert gym_class["description"] == "Physical education and sports activities"
        assert gym_class["schedule"] == "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM"
        assert gym_class["max_participants"] == 30
        assert gym_class["participants"] == ["john@mergington.edu", "olivia@mergington.edu"]
    
    def test_get_activities_basketball_team_correct_data(self, client):
        """Test that Basketball Team has correct data."""
        response = client.get("/activities")
        activities = response.json()
        basketball = activities["Basketball Team"]
        
        assert basketball["description"] == "Practice and compete in basketball games"
        assert basketball["schedule"] == "Tuesdays and Thursdays, 4:00 PM - 6:00 PM"
        assert basketball["max_participants"] == 15
        assert basketball["participants"] == ["alex@mergington.edu"]
    
    def test_get_activities_soccer_club_correct_data(self, client):
        """Test that Soccer Club has correct data."""
        response = client.get("/activities")
        activities = response.json()
        soccer = activities["Soccer Club"]
        
        assert soccer["description"] == "Train and play soccer matches"
        assert soccer["schedule"] == "Wednesdays and Saturdays, 3:00 PM - 5:00 PM"
        assert soccer["max_participants"] == 22
        assert soccer["participants"] == ["liam@mergington.edu", "ava@mergington.edu"]
    
    def test_get_activities_art_club_correct_data(self, client):
        """Test that Art Club has correct data."""
        response = client.get("/activities")
        activities = response.json()
        art_club = activities["Art Club"]
        
        assert art_club["description"] == "Explore painting, drawing, and other visual arts"
        assert art_club["schedule"] == "Mondays, 3:30 PM - 5:00 PM"
        assert art_club["max_participants"] == 18
        assert art_club["participants"] == ["isabella@mergington.edu"]
    
    def test_get_activities_drama_club_correct_data(self, client):
        """Test that Drama Club has correct data."""
        response = client.get("/activities")
        activities = response.json()
        drama = activities["Drama Club"]
        
        assert drama["description"] == "Act in plays and learn theater skills"
        assert drama["schedule"] == "Tuesdays, 4:00 PM - 5:30 PM"
        assert drama["max_participants"] == 20
        assert drama["participants"] == ["mason@mergington.edu", "charlotte@mergington.edu"]
    
    def test_get_activities_debate_club_correct_data(self, client):
        """Test that Debate Club has correct data."""
        response = client.get("/activities")
        activities = response.json()
        debate = activities["Debate Club"]
        
        assert debate["description"] == "Develop argumentation and public speaking skills"
        assert debate["schedule"] == "Thursdays, 3:30 PM - 4:30 PM"
        assert debate["max_participants"] == 16
        assert debate["participants"] == ["ethan@mergington.edu"]
    
    def test_get_activities_science_club_correct_data(self, client):
        """Test that Science Club has correct data."""
        response = client.get("/activities")
        activities = response.json()
        science = activities["Science Club"]
        
        assert science["description"] == "Conduct experiments and explore scientific concepts"
        assert science["schedule"] == "Fridays, 4:00 PM - 5:30 PM"
        assert science["max_participants"] == 25
        assert science["participants"] == ["harper@mergington.edu", "logan@mergington.edu"]
    
    def test_get_activities_participants_is_list(self, client):
        """Test that participants field is always a list."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list), \
                f"{activity_name} has non-list participants"
    
    def test_get_activities_max_participants_is_int(self, client):
        """Test that max_participants field is always an integer."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["max_participants"], int), \
                f"{activity_name} has non-int max_participants"
