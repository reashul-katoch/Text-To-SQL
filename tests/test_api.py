from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_token(username, password):
    response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": password
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_invalid_login():
    response = client.post(
        "/auth/login",
        json={
            "username": "admin",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_viewer_can_read_customers():
    token = get_token(
        "viewer",
        "viewer123"
    )

    response = client.get(
        "/customers",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert "customers" in response.json()


def test_viewer_cannot_write():
    token = get_token(
        "viewer",
        "viewer123"
    )

    response = client.post(
        "/admin/test-write",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


def test_admin_can_write():
    token = get_token(
        "admin",
        "admin123"
    )

    response = client.post(
        "/admin/test-write",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Write operation permitted"


def test_unauthorized_customer_access():
    response = client.get("/customers")

    assert response.status_code == 401