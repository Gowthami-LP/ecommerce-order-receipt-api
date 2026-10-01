from typing import List

from fastapi import APIRouter, HTTPException, status

from app.repositories.order_repository import OrderRepository
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, summary="Create an order")
def create_order(order: OrderCreate):
    """Create a new order in the orders collection."""
    if OrderRepository.get_order_by_id(order.order_id):
        raise HTTPException(status_code=400, detail="Order already exists")

    order_data = {
        "_id": order.order_id,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "status": order.status,
        "order_date": order.order_date,
    }
    OrderRepository.create_order(order_data)
    return OrderResponse(
        order_id=order_data["_id"],
        user_id=order_data["user_id"],
        product_id=order_data["product_id"],
        quantity=order_data["quantity"],
        status=order_data["status"],
        order_date=order_data["order_date"],
    )


@router.get("/{order_id}", response_model=OrderResponse, summary="Get an order")
def get_order(order_id: str):
    """Fetch an order by its ID."""
    order = OrderRepository.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderResponse(**order)


@router.get("", response_model=List[OrderResponse], summary="List all orders")
def list_orders():
    """Return all orders in the orders collection."""
    return [OrderResponse(**order) for order in OrderRepository.get_all_orders()]


@router.put("/{order_id}", response_model=OrderResponse, summary="Update an order")
def update_order(order_id: str, order: OrderUpdate):
    """Update details of an existing order."""
    existing = OrderRepository.get_order_by_id(order_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Order not found")

    update_data = order.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No order fields provided for update")

    OrderRepository.update_order(order_id, update_data)
    updated = OrderRepository.get_order_by_id(order_id)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update order")
    return OrderResponse(**updated)


@router.delete("/{order_id}", status_code=status.HTTP_200_OK, summary="Delete an order")
def delete_order(order_id: str):
    """Delete an order by ID."""
    existing = OrderRepository.get_order_by_id(order_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Order not found")

    OrderRepository.delete_order(order_id)
    return {"message": "Order deleted successfully"}
