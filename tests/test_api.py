import os
import sqlite3

import pytest
from fastapi.testclient import TestClient

from src.api.main import app, settings

client = TestClient(app)


def test_api_validation_error():
    ERROR_CODE = 422
    """
    Sprawdza, czy API zwraca bład 422,
    gdy wyślemy pusty JSON lub błędne typy danych.
    """
    response = client.post("/predict", json={})
    assert response.status_code == ERROR_CODE

    response = client.post("/predict", json={"cap-shape": "x"})
    assert response.status_code == ERROR_CODE


def test_predict_saves_to_database():
    """
    Wysyła poprawny payload, sprawdza status 200
    i weryfiuje, czy w bazie SQLite pojawil sie nowy rekord
    """
    payload = {
        "cap-shape": "x",
        "cap-surface": "s",
        "cap-color": "y",
        "bruises": "t",
        "odor": "a",
        "gill-attachment": "f",
        "gill-spacing": "c",
        "gill-size": "b",
        "gill-color": "k",
        "stalk-shape": "e",
        "stalk-root": "c",
        "stalk-surface-above-ring": "s",
        "stalk-surface-below-ring": "s",
        "stalk-color-above-ring": "w",
        "stalk-color-below-ring": "w",
        "veil-type": "p",
        "veil-color": "w",
        "ring-number": "o",
        "ring-type": "p",
        "spore-print-color": "n",
        "population": "n",
        "habitat": "g",
    }

    with TestClient(app) as client:
        response = client.post("/predict", json=payload)
        CODE_503 = 503
        CODE_200 = 200

        if response.status_code == CODE_503:
            pytest.skip("Model nie jest załadowany - pomijam test integracyjny.")

        assert response.status_code == CODE_200, f"Błąd API: {response.text}"

        data = response.json()
        assert "prediction" in data
        assert "model_version" in data

        assert os.path.exists(
            settings.DB_NAME
        ), "Plik bazy danych nie został utworzony!"

        with sqlite3.connect(settings.DB_NAME) as con:
            cursor = con.cursor()
            cursor.execute(
                "SELECT payload, prediction FROM predictions ORDER BY id DESC LIMIT 1"
            )
            row = cursor.fetchone()

            assert row is not None, "Nie znaleziono rekordu w bazie!"

            db_payload, db_prediction = row
            assert "cap-shape" in db_payload
            assert '"odor": "a"' in db_payload
            assert db_prediction == str(data["prediction"])
