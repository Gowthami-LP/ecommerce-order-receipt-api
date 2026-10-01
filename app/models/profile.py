from pydantic import BaseModel, EmailStr, Field

from app.models.address import Address


class Profile(BaseModel):
    """Profile model representing a customer in the profiles collection."""

    user_id: str = Field(..., min_length=3)
    name: str = Field(..., min_length=1)
    email: EmailStr
    phone: str = Field(..., min_length=7)
    address: Address
