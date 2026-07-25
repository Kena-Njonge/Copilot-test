import copy

from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


def reset_activities():
    app_module.activities = copy.deepcopy(app_module.ORIGINAL_ACTIVITIES)


def test_get_activities_returns_activity_data():
    # Arrange
    reset_activities()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["description"]


def test_signup_for_new_student_succeeds():
    # Arrange
    reset_activities()
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in app_module.activities["Chess Club"]["participants"]


def test_duplicate_signup_returns_400_and_does_not_duplicate():
    # Arrange
    reset_activities()
    email = "michael@mergington.edu"

    # Act
    first_response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )
    second_response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    # Assert
    assert first_response.status_code == 400
    assert second_response.status_code == 400
    assert app_module.activities["Chess Club"]["participants"].count(email) == 1
