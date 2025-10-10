from fastapi.testclient import TestClient
import pytest

from src.app import app, activities

client = TestClient(app)


def test_get_activities_returns_200_and_structure():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # should be a dict containing known activity
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "test_student@mergington.edu"

    # ensure clean start: remove if exists
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # duplicate signup should fail
    resp_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_dup.status_code == 400

    # unregister
    resp_unreg = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp_unreg.status_code == 200
    assert email not in activities[activity]["participants"]

    # unregistering again should return 404
    resp_unreg2 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp_unreg2.status_code == 404

