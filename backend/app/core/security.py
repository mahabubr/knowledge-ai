import os
from datetime import datetime, timezone, timedelta
import bcrypt
from jose import jwt


SECRET_KEY = os.getenv("JWT_SECRET", "CHANGE_THIS_SECRET_KEY")
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False


def create_access_token(email: str, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=24)

    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

