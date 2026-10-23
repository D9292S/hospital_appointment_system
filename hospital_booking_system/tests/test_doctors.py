def test_create_doctor_returns_created(client):
    response = client.post("/doctors", json={
        "name": "Dr Meera",
        "specialization": "Neurology",
        "consultation_fee": 700
    })
    assert response.status_code == 201
    assert response.json()["id"] > 0


def test_missing_doctor_returns_404(client):
    response = client.get("/doctors/9999")
    assert response.status_code == 404


def test_negative_fee_is_rejected(client):
    response = client.post("/doctors", json={
        "name": "Dr Negative",
        "specialization": "Cardiology",
        "consultation_fee": -10
    })
    assert response.status_code == 422


def test_specialization_search_is_case_insensitive(client, doctor):
    response = client.get("/doctors", params={"specialization": "  cardiology "})
    assert response.status_code == 200
    assert len(response.json()) == 1
