def test_protected_route_requires_auth(client):
    r = client.get("/api/v1/auth/me")
    assert r.status_code == 401


def test_admin_route_requires_auth(client):
    r = client.get("/api/v1/admin/users")
    assert r.status_code == 401


def test_login_success(client, customer):
    r = client.post(
        "/api/v1/auth/login",
        json={"email": "customer@test.com", "password": "customer123"},
    )
    assert r.status_code == 200
    body = r.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_wrong_password(client, customer):
    r = client.post(
        "/api/v1/auth/login",
        json={"email": "customer@test.com", "password": "WRONG"},
    )
    assert r.status_code == 401


def test_login_unknown_email(client):
    r = client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@test.com", "password": "whatever123"},
    )
    assert r.status_code == 401


def test_register_forces_customer_role(client):
    r = client.post(
        "/api/v1/auth/register",
        json={"email": "new@test.com", "password": "newpass123"},
    )
    assert r.status_code == 201
    assert r.json()["role"] == "customer"