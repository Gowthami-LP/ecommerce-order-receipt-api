from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Invoice(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    order_id: str
    invoice_number: str
    subtotal: float = 0.0
    tax: float = 0.0
    discount: float = 0.0
    shipping_charge: float = 0.0
    total_amount: float = 0.0
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(populate_by_name=True)
