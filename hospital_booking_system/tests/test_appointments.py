from datetime import datetime, timedelta


def future_time(hours=2, minutes=0):
    return (datetime.now().replace(second=0, microsecond=0) + timedelta(hours=hours, minutes=minutes)).isoformat()


def book(client, doctor, patient, appointment_time):
    return client.post("/appointments", json={
        "doctor_id": doctor["id"],
        "patient_id": patient["id"],
        "appointment_time": appointment_time,
    })


def test_booking_past_time_is_rejected(client, doctor, patient):
    past = (datetime.now() - timedelta(days=1)).replace(microsecond=0).isoformat()
    response = book(client, doctor, patient, past)
    assert response.status_code in (400, 422)


def test_cancel_is_persisted(client, doctor, patient):
    created = book(client, doctor, patient, future_time()).json()
    response = client.patch(f"/appointments/{created['id']}/cancel")
    assert response.status_code == 200
    fetched = client.get("/appointments").json()
    item = next(item for item in fetched if item["id"] == created["id"])
    assert item["status"] == "cancelled"


def test_reschedule_conflict_is_rejected(client, doctor, patient):
    first = book(client, doctor, patient, future_time()).json()
    second = book(client, doctor, patient, future_time(hours=3)).json()
    response = client.patch(
        f"/appointments/{second['id']}/reschedule",
        json={"appointment_time": first["appointment_time"]},
    )
    assert response.status_code == 409


def test_overlapping_booking_is_rejected_but_adjacent_is_allowed(client, doctor, patient):
    start = datetime.now().replace(second=0, microsecond=0) + timedelta(days=1)
    start = start.replace(hour=10, minute=0)
    first = book(client, doctor, patient, start.isoformat())
    assert first.status_code == 201

    overlap = book(client, doctor, patient, (start + timedelta(minutes=15)).isoformat())
    assert overlap.status_code == 409

    adjacent = book(client, doctor, patient, (start + timedelta(minutes=30)).isoformat())
    assert adjacent.status_code == 201


def test_status_transition_rules(client, doctor, patient):
    created = book(client, doctor, patient, future_time()).json()
    cancelled = client.patch(
        f"/appointments/{created['id']}/status",
        params={"status": "cancelled"},
    )
    assert cancelled.status_code == 200

    invalid_transition = client.patch(
        f"/appointments/{created['id']}/status",
        params={"status": "booked"},
    )
    assert invalid_transition.status_code == 409

    invalid_status = client.patch(
        f"/appointments/{created['id']}/status",
        params={"status": "banana"},
    )
    assert invalid_status.status_code == 422
