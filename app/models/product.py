from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Product(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    description: str
    price: float
    category: str
    stock: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(populate_by_name=True)
