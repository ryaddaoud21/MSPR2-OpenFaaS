import requests

base_url = "http://127.0.0.1:8080/function"

def test_create_user():
    r = requests.post(f"{base_url}/create-user", json={
        "username": "testuser",
        "password": "Test@1234",
        "mfa": ""
    })
    print("Create user:", r.json())

def test_login():
    r = requests.post(f"{base_url}/login", json={
        "username": "testuser",
        "password": "Test@1234"
    })
    print("Login:", r.json())

def test_generate_password():
    r = requests.post(f"{base_url}/generate-password", json={
        "username": "testuser"
    })
    print("Generate password:", r.json())

def test_generate_2fa():
    r = requests.post(f"{base_url}/generate-2fa", json={
        "username": "testuser"
    })
    print("Generate 2FA:", r.json())

def test_verify_2fa():
    token = input("Enter TOTP from Google Authenticator: ")
    r = requests.post(f"{base_url}/verify-2fa", json={
        "username": "testuser",
        "token": token
    })
    print("Verify 2FA:", r.json())

if __name__ == "__main__":
    test_create_user()
    test_login()
    test_generate_password()
    test_generate_2fa()
    test_verify_2fa()