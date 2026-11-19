import pytest

import app as catshop


@pytest.fixture
def client(monkeypatch, tmp_path):
    monkeypatch.setattr(catshop, "DATABASE_URL", None)
    monkeypatch.setattr(catshop, "COUNTER_FILE", tmp_path / "data" / "visits.txt")
    with catshop.app.test_client() as client:
        yield client


def test_health_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_data(as_text=True) == "ok\n"


def test_ready_reports_file_store(client):
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.get_json() == {
        "ready": True,
        "store": f"file:{catshop.COUNTER_FILE}",
    }


def test_ready_returns_503_when_counter_directory_cannot_be_created(client):
    catshop.COUNTER_FILE.parent.write_text("A file occupies the directory path")

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.get_json()["ready"] is False


def test_visits_increments_and_persists_the_counter(client):
    first_visit = client.get("/visits")
    second_visit = client.get("/visits")

    assert first_visit.status_code == 200
    assert first_visit.get_json() == {"visits": 1, "store": "file"}
    assert second_visit.status_code == 200
    assert second_visit.get_json() == {"visits": 2, "store": "file"}
    assert catshop.COUNTER_FILE.read_text() == "2"


def test_visits_resumes_from_an_existing_counter(client):
    catshop.COUNTER_FILE.parent.mkdir()
    catshop.COUNTER_FILE.write_text("100")

    response = client.get("/visits")

    assert response.status_code == 200
    assert response.get_json() == {"visits": 101, "store": "file"}
