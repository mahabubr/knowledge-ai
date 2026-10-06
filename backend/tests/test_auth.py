import pytest
from jose import jwt
from app.core.security import SECRET_KEY, ALGORITHM, hash_password, verify_password, create_access_token
from app.models.user import User


def test_signup_success(client, db_session):
    """Test successful user registration."""
    payload = {
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "strongpassword123",
    }
    response = client.post("/auth/signup", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Signup successful"
    assert "id" in data
    assert isinstance(data["id"], int)

    # Verify user exists in database with hashed password
    user = db_session.query(User).filter(User.email == "test@example.com").first()
    assert user is not None
    assert user.full_name == "Test User"
    assert user.password != "strongpassword123"
    assert verify_password("strongpassword123", user.password) is True


def test_signup_with_name_alias(client, db_session):
    """Test registration using 'name' field instead of 'full_name'."""
    payload = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "password": "securepassword",
    }
    response = client.post("/auth/signup", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Signup successful"

    user = db_session.query(User).filter(User.email == "jane@example.com").first()
    assert user is not None
    assert user.full_name == "Jane Doe"


def test_signup_duplicate_email(client):
    """Test registration with an already existing email."""
    payload = {
        "full_name": "First User",
        "email": "duplicate@example.com",
        "password": "password123",
    }
    resp1 = client.post("/auth/signup", json=payload)
    assert resp1.status_code == 201

    # Attempt to signup again with identical email
    resp2 = client.post("/auth/signup", json=payload)
    assert resp2.status_code == 400
    assert resp2.json()["detail"] == "Email already registered"


def test_signup_case_insensitive_duplicate_email(client):
    """Test duplicate check is case-insensitive for emails."""
    payload1 = {
        "full_name": "User One",
        "email": "case.test@example.com",
        "password": "password123",
    }
    resp1 = client.post("/auth/signup", json=payload1)
    assert resp1.status_code == 201

    payload2 = {
        "full_name": "User Two",
        "email": "CASE.TEST@example.com",
        "password": "password456",
    }
    resp2 = client.post("/auth/signup", json=payload2)
    assert resp2.status_code == 400
    assert resp2.json()["detail"] == "Email already registered"


@pytest.mark.parametrize(
    "invalid_payload, expected_detail_field",
    [
        ({"full_name": "No Email", "password": "password123"}, "email"),
        ({"email": "not-an-email", "full_name": "Bad Email", "password": "password123"}, "email"),
        ({"email": "valid@example.com", "full_name": "Short Pass", "password": "123"}, "password"),
        ({"email": "valid@example.com", "password": "password123"}, "full_name"),
    ],
)
def test_signup_validation_errors(client, invalid_payload, expected_detail_field):
    """Test signup validation constraints."""
    response = client.post("/auth/signup", json=invalid_payload)
    assert response.status_code == 422


def test_login_success(client):
    """Test successful login returns valid JWT token."""
    # Register first
    signup_payload = {
        "full_name": "Login User",
        "email": "login@example.com",
        "password": "mypassword123",
    }
    signup_resp = client.post("/auth/signup", json=signup_payload)
    assert signup_resp.status_code == 201

    # Login
    login_payload = {
        "email": "login@example.com",
        "password": "mypassword123",
    }
    login_resp = client.post("/auth/login", json=login_payload)
    assert login_resp.status_code == 200
    data = login_resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Decode and verify JWT token payload
    decoded = jwt.decode(data["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "login@example.com"
    assert "exp" in decoded


def test_login_case_insensitive_email(client):
    """Test login works regardless of email case."""
    signup_payload = {
        "full_name": "Case User",
        "email": "my.name@example.com",
        "password": "secretpassword",
    }
    signup_resp = client.post("/auth/signup", json=signup_payload)
    assert signup_resp.status_code == 201

    # Login with uppercase email
    login_payload = {
        "email": "MY.NAME@EXAMPLE.COM",
        "password": "secretpassword",
    }
    login_resp = client.post("/auth/login", json=login_payload)
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()


def test_login_user_not_found(client):
    """Test login with an unregistered email."""
    login_payload = {
        "email": "nonexistent@example.com",
        "password": "anypassword",
    }
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_login_invalid_password(client):
    """Test login with an incorrect password."""
    signup_payload = {
        "full_name": "Target User",
        "email": "target@example.com",
        "password": "correctpassword",
    }
    signup_resp = client.post("/auth/signup", json=signup_payload)
    assert signup_resp.status_code == 201

    # Attempt login with wrong password
    login_payload = {
        "email": "target@example.com",
        "password": "wrongpassword",
    }
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid password"


def test_login_validation_errors(client):
    """Test login with invalid body payload."""
    # Invalid email format
    resp1 = client.post("/auth/login", json={"email": "not-valid", "password": "pass"})
    assert resp1.status_code == 422

    # Missing password
    resp2 = client.post("/auth/login", json={"email": "test@example.com"})
    assert resp2.status_code == 422


def test_security_utilities():
    """Unit tests for hashing, verification, and tokens."""
    pwd = "supersecretpassword"
    hashed = hash_password(pwd)

    assert hashed != pwd
    assert verify_password(pwd, hashed) is True
    assert verify_password("wrongpassword", hashed) is False
    assert verify_password(pwd, "invalid_hash_string") is False

    token = create_access_token("user@test.com")
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "user@test.com"
