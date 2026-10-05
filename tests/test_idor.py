def test_user_cannot_edit_another_users_profile(client, customer_token, admin):
    # admin exists with id != customer id; customer tries to edit admin
    r = client.patch(
        f"/api/v1/auth/users/{admin.id}/profile",
        json={"full_name": "Hacked"},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert r.status_code == 403


def test_user_can_edit_own_profile(client, customer_token, customer):
    r = client.patch(
        f"/api/v1/auth/users/{customer.id}/profile",
        json={"full_name": "New Name"},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert r.status_code == 200
    assert r.json()["full_name"] == "New Name"


def test_admin_can_edit_any_profile(client, admin_token, customer):
    r = client.patch(
        f"/api/v1/auth/users/{customer.id}/profile",
        json={"full_name": "Managed by admin"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert r.status_code == 200
    assert r.json()["full_name"] == "Managed by admin"