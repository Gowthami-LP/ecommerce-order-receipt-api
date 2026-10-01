from typing import Optional

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    """Request schema for creating a product."""

    product_id: str = Field(..., min_length=3)
    name: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    price: float = Field(..., ge=0)
    brand: str = Field(..., min_length=1)
    stock: int = Field(..., ge=0)


class ProductUpdate(BaseModel):
    """Partial update schema for a product."""

    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = Field(default=None, ge=0)
    brand: Optional[str] = None
    stock: Optional[int] = Field(default=None, ge=0)


class ProductResponse(BaseModel):
    """Product information returned to the client."""

    model_config = ConfigDict(populate_by_name=True)

    product_id: str = Field(validation_alias=AliasChoices("_id", "product_id"))
    name: str
    category: str
    price: float
    brand: str
    stock: int
