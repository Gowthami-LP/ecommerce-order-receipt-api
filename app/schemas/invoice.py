from typing import Optional

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class InvoiceCreate(BaseModel):
    """Request schema for creating an invoice."""

    invoice_id: str = Field(..., min_length=3)
    order_id: str = Field(..., min_length=3)
    subtotal: float = Field(..., ge=0)
    tax: float = Field(..., ge=0)
    discount: float = Field(..., ge=0)
    shipping: float = Field(..., ge=0)
    total: float = Field(..., ge=0)
    payment_status: str = Field(..., min_length=1)


class InvoiceUpdate(BaseModel):
    """Partial update schema for an invoice."""

    subtotal: Optional[float] = Field(default=None, ge=0)
    tax: Optional[float] = Field(default=None, ge=0)
    discount: Optional[float] = Field(default=None, ge=0)
    shipping: Optional[float] = Field(default=None, ge=0)
    total: Optional[float] = Field(default=None, ge=0)
    payment_status: Optional[str] = None


class InvoiceResponse(BaseModel):
    """Invoice information returned to the client."""

    model_config = ConfigDict(populate_by_name=True)

    invoice_id: str = Field(validation_alias=AliasChoices("_id", "invoice_id"))
    order_id: str = Field(validation_alias=AliasChoices("order_id",))
    subtotal: float
    tax: float
    discount: float
    shipping: float
    total: float
    payment_status: str
