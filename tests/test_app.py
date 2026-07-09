from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module
from src.app import app


BASE_ACTIVITIES = deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = deepcopy(BASE_ACTIVITIES)
    yield
    app_module.activities = deepcopy(BASE_ACTIVITIES)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_student_cannot_sign_up_twice_for_same_activity(client):
    # Arrange
    email = "dup@example.com"
    activity_name = "Chess Club"

    # Act
    first_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    second_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert "already signed up" in second_response.json()["detail"].lower()


def test_signup_updates_activity_participants(client):
    # Arrange
    email = "state@example.com"
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
