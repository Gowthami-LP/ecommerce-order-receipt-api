from typing import Optional

from pydantic import AliasChoices, BaseModel, ConfigDict, EmailStr, Field


class AddressSchema(BaseModel):
    city: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)


class ProfileCreate(BaseModel):
    """Request schema for creating a profile."""

    user_id: str = Field(..., min_length=3)
    name: str = Field(..., min_length=1)
    email: EmailStr
    phone: str = Field(..., min_length=7)
    address: AddressSchema


class ProfileUpdate(BaseModel):
    """Partial update schema for a profile."""

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[AddressSchema] = None


class ProfileResponse(BaseModel):
    """Profile information returned to the client."""

    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(validation_alias=AliasChoices("_id", "user_id"))
    name: str
    email: EmailStr
    phone: str
    address: AddressSchema
