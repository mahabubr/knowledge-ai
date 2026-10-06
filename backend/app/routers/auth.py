from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.user import SignupRequest, LoginRequest, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: SignupRequest, db: Session = Depends(get_db)):
    email = user.email.lower().strip()
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_user = User(
        full_name=user.full_name.strip(),
        email=email,
        password=hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Signup successful", "id": new_user.id}


@router.post("/login", response_model=TokenResponse)
def login(user: LoginRequest, db: Session = Depends(get_db)):
    email = user.email.lower().strip()
    db_user = db.query(User).filter(User.email == email).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
        )

    token = create_access_token(db_user.email)

    return {"access_token": token, "token_type": "bearer"}

