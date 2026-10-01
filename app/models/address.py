from __future__ import annotations

from pydantic import BaseModel, Field


class Address(BaseModel):
    """Address model used by profile records."""

    city: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)
