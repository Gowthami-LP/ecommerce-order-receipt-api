from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Order(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    shipping_address_id: Optional[str] = None
    billing_address_id: Optional[str] = None
    status: str = "pending"
    subtotal: float = 0.0
    tax: float = 0.0
    discount: float = 0.0
    shipping_charge: float = 0.0
    total_amount: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(populate_by_name=True)
