def test_customer_cannot_access_admin_panel(client, customer_token):
    r = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert r.status_code == 403


def test_admin_can_access_admin_panel(client, admin_token):
    r = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert r.status_code == 200


def test_admin_can_access_own_profile(client, admin_token):
    r = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert r.status_code == 200
    assert r.json()["role"] == "admin"