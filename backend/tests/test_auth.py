# File: tests/test_auth.py

def test_register_and_login(client):
    # 1) Register
    register_payload = {"email": "testuser@example.com", "password": "secretpass"}
    reg_res = client.post("/auth/register", json=register_payload)
    assert reg_res.status_code == 200, reg_res.text
    # optionally check reg_res.json() if it returns user info

    # 2) Login
    login_payload = {"email": "testuser@example.com", "password": "secretpass"}
    login_res = client.post("/auth/login", json=login_payload)
    assert login_res.status_code == 200, login_res.text
    data = login_res.json()
    assert "access_token" in data
    token = data["access_token"]
    assert token, "Token should not be empty"

def test_auth_me(client):
    # 1) Register & login
    register_payload = {"email": "myme@example.com", "password": "mypassword"}
    client.post("/auth/register", json=register_payload)
    login_res = client.post("/auth/login", json=register_payload)
    token = login_res.json()["access_token"]

    # 2) Call /auth/me with the token
    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/auth/me", headers=headers)
    assert me_res.status_code == 200, me_res.text
    me_data = me_res.json()
    assert me_data["email"] == "myme@example.com"
