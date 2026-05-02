"""
Tests for the GET / endpoint.

This module tests the root endpoint redirect functionality.
"""

import pytest


class TestRedirect:
    """Test suite for GET / endpoint."""
    
    def test_root_endpoint_redirects(self, client):
        """Test that GET / returns a redirect (status 307)."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
    
    def test_root_endpoint_redirects_to_static_index(self, client):
        """Test that GET / redirects to /static/index.html."""
        response = client.get("/", follow_redirects=False)
        assert "location" in response.headers
        assert response.headers["location"] == "/static/index.html"
    
    def test_root_endpoint_with_follow_redirects(self, client):
        """Test that following the redirect returns the index.html page."""
        response = client.get("/", follow_redirects=True)
        # The response should contain the index.html content
        # Status should be 200 after following redirect
        assert response.status_code == 200
    
    def test_root_endpoint_absolute_redirect_url(self, client):
        """Test that the redirect location header is a relative URL."""
        response = client.get("/", follow_redirects=False)
        location = response.headers["location"]
        # Should be a relative path
        assert location.startswith("/")
        assert "mergington" not in location.lower()  # Not an absolute URL
