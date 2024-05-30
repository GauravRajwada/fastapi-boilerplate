from pydantic import BaseModel, validator
from typing import Optional
import re

class CreateUser(BaseModel):
    name: str
    email: str
    password: str
    mobile: str
    preferred_categories: Optional[list[str]]

    # Validate the email
    @validator('email')
    def email_validator(cls, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        return email

    # Validate the mobile number
    @validator('mobile')
    def mobile_validator(cls, mobile):
        if not re.match(r"^[6-9]\d{9}$", mobile):
            raise ValueError("Invalid mobile number format")
        return mobile
    