from fastapi.testclient import TestClient

from src.app import app


def test_student_cannot_sign_up_twice_for_same_activity():
    client = TestClient(app)
    email = "dup@example.com"

    first_response = client.post("/activities/Chess Club/signup", params={"email": email})
    second_response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert "already signed up" in second_response.json()["detail"].lower()


def test_signup_updates_activity_participants():
    client = TestClient(app)
    email = "state@example.com"

    response = client.post("/activities/Chess Club/signup", params={"email": email})
    activities = client.get("/activities").json()

    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]
