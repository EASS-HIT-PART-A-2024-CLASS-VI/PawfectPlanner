# File: tests/test_reminders.py
import datetime

def _auth_headers(client, email="reminderuser@example.com", password="rempass"):
    client.post("/auth/register", json={"email": email, "password": password})
    login_res = client.post("/auth/login", json={"email": email, "password": password})
    return {"Authorization": f"Bearer {login_res.json()['access_token']}"}

def test_create_reminder(client):
    headers = _auth_headers(client)

    # create a pet first
    pet_res = client.post("/pets", json={
        "name": "ReminderPet",
        "type": "dog",
        "breed": "Husky",
        "owner_id": 1
    }, headers=headers)
    pet_id = pet_res.json()["id"]

    # create a reminder
    payload = {
        "title": "Vet Appointment",
        "date": "2025-06-11",
        "time": "09:30",
        "repetition": "once",
        "location": "Local Vet",
        "notes": "Check vaccines",
        "pet_id": pet_id
    }
    res = client.post("/reminders", json=payload, headers=headers)
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["title"] == "Vet Appointment"
    assert data["pet_id"] == pet_id

def test_list_reminders(client):
    headers = _auth_headers(client, "listrem@example.com")

    # create 2
    client.post("/reminders", json={
        "title": "Reminder A",
        "date": "2025-03-07",
        "time": "08:00",
        "repetition": "once"
    }, headers=headers)
    client.post("/reminders", json={
        "title": "Reminder B",
        "date": "2025-03-08",
        "time": "10:15",
        "repetition": "1 weeks"
    }, headers=headers)

    res = client.get("/reminders", headers=headers)
    assert res.status_code == 200
    arr = res.json()
    assert len(arr) >= 2

def test_delete_reminder(client):
    headers = _auth_headers(client, "delrem@example.com")

    # create
    create_res = client.post("/reminders", json={
        "title": "ToDelete",
        "date": "2025-07-01",
        "time": "09:00",
        "repetition": "once"
    }, headers=headers)
    reminder_id = create_res.json()["id"]

    # delete
    del_res = client.delete(f"/reminders/{reminder_id}", headers=headers)
    assert del_res.status_code == 200
    assert del_res.json()["detail"] == "Reminder deleted successfully."

    # confirm gone
    list_res = client.get("/reminders", headers=headers)
    for r in list_res.json():
        assert r["id"] != reminder_id

def test_download_ics(client):
    headers = _auth_headers(client, "icsrem@example.com")

    # create
    create_res = client.post("/reminders", json={
        "title": "ICS Test",
        "date": "2025-12-25",
        "time": "08:30",
        "repetition": "once"
    }, headers=headers)
    reminder_id = create_res.json()["id"]

    # download ICS
    ics_res = client.get(f"/reminders/download/{reminder_id}", headers=headers)
    assert ics_res.status_code == 200
    assert ics_res.headers["Content-Type"] == "text/calendar"
    # Optionally check ics_res.text for certain iCalendar fields
    assert "BEGIN:VCALENDAR" in ics_res.text
    assert "SUMMARY:ICS Test" in ics_res.text
