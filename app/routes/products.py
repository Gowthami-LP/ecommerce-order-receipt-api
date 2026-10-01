from typing import List

from fastapi import APIRouter, HTTPException, status

from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.post("", response_model=ProductResponse, summary="Create a product")
def create_product(product: ProductCreate):
    """Create one product in the products collection."""
    if ProductRepository.get_product_by_id(product.product_id):
        raise HTTPException(status_code=400, detail="Product already exists")

    product_data = {
        "_id": product.product_id,
        "name": product.name,
        "category": product.category,
        "price": product.price,
        "brand": product.brand,
        "stock": product.stock,
    }
    ProductRepository.create_product(product_data)
    return ProductResponse(
        product_id=product_data["_id"],
        name=product_data["name"],
        category=product_data["category"],
        price=product_data["price"],
        brand=product_data["brand"],
        stock=product_data["stock"],
    )


@router.get("/{product_id}", response_model=ProductResponse, summary="Get a product")
def get_product(product_id: str):
    """Fetch a product by its ID."""
    product = ProductRepository.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse(**product)


@router.get("", response_model=List[ProductResponse], summary="List all products")
def list_products():
    """Return all products in the products collection."""
    return [ProductResponse(**product) for product in ProductRepository.get_all_products()]


@router.put("/{product_id}", response_model=ProductResponse, summary="Update a product")
def update_product(product_id: str, product: ProductUpdate):
    """Update a product with partial fields."""
    existing = ProductRepository.get_product_by_id(product_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No product fields provided for update")

    ProductRepository.update_product(product_id, update_data)
    updated = ProductRepository.get_product_by_id(product_id)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update product")
    return ProductResponse(**updated)


@router.delete("/{product_id}", status_code=status.HTTP_200_OK, summary="Delete a product")
def delete_product(product_id: str):
    """Delete a product by product ID."""
    existing = ProductRepository.get_product_by_id(product_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")

    ProductRepository.delete_product(product_id)
    return {"message": "Product deleted successfully"}
