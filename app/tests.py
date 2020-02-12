from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_main_error_status_code():
    response = client.get("/api/")
    assert response.status_code == 404


def test_main_success_status_code():
    response = client.get("/api/norge")
    assert response.status_code == 200

def test_get_links_by_team_status_code():
    response = client.get('/api/norge/teams/Brann')
    assert response.status_code == 200

def test_get_links_by_league_status_code():
    response = client.get('/api/norge/league/eliteserien')
    assert response.status_code == 200
