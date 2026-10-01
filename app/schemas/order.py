from typing import Literal, Optional

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class OrderCreate(BaseModel):
    """Request schema for creating an order."""

    order_id: str = Field(..., min_length=3)
    user_id: str = Field(..., min_length=3)
    product_id: str = Field(..., min_length=3)
    quantity: int = Field(..., gt=0)
    status: Literal["pending", "confirmed", "processing", "shipped", "delivered", "cancelled"] = "pending"
    order_date: str = Field(..., min_length=1)


class OrderUpdate(BaseModel):
    """Partial update schema for an order."""

    user_id: Optional[str] = None
    product_id: Optional[str] = None
    quantity: Optional[int] = Field(default=None, gt=0)
    status: Optional[Literal["pending", "confirmed", "processing", "shipped", "delivered", "cancelled"]] = None
    order_date: Optional[str] = None


class OrderResponse(BaseModel):
    """Order information returned to the client."""

    model_config = ConfigDict(populate_by_name=True)

    order_id: str = Field(validation_alias=AliasChoices("_id", "order_id"))
    user_id: str = Field(validation_alias=AliasChoices("user_id",))
    product_id: str = Field(validation_alias=AliasChoices("product_id",))
    quantity: int
    status: str
    order_date: str
