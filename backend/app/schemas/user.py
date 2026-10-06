from pydantic import BaseModel, EmailStr, Field, AliasChoices, ConfigDict


class SignupRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    full_name: str = Field(validation_alias=AliasChoices("full_name", "name"))
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

