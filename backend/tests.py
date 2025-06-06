from datetime import datetime

import models
from db import get_db


def test_get_available_currencies(client):
    db = next(get_db())
    test_currency = models.Currency(
        name="Test Dollar", code="TST", mid=1.23, date=datetime(2024, 1, 1)
    )
    db.add(test_currency)
    db.commit()

    response = client.get("/currencies")
    assert response.status_code == 200
    data = response.json()
    assert any(c["code"] == "TST" for c in data)


def test_get_currency_by_date(client):
    response = client.get("/currencies/2024-01-01")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["code"] == "TST"
    assert data[0]["date"] == "2024-01-01"


def test_get_currency_by_invalid_date(client):
    response = client.get("/currencies/invalid-date")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid date format. Use YYYY-MM-DD."


def test_get_currency_by_unknown_date(client):
    response = client.get("/currencies/1990-01-01")
    assert response.status_code == 404
    assert response.json()["detail"] == "No currency data for the given date."
