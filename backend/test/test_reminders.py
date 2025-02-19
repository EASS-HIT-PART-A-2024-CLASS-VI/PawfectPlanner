from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestReminders:
    """
    Tests for reminders functionality.
    """

    def test_create_reminder(self):
        """
        Test creating a reminder.
        """
        response = client.post(
            "/api/reminders",
            json={"title": "Vet Appointment", "date": "2024-01-30", "pet_id": 1},
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["title"] == "Vet Appointment"

    def test_fetch_reminders(self):
        """
        Test fetching reminders.
        """
        response = client.get("/api/reminders")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_delete_reminder(self):
        """
        Test deleting a reminder.
        """
        # Assuming a reminder with ID 1 exists
        response = client.delete("/api/reminders/1")
        assert response.status_code == 200
        assert response.json() == {"detail": "Reminder deleted successfully."}
