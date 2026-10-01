from __future__ import annotations

from typing import Any, Dict

from fastapi import HTTPException

from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.profile_repository import ProfileRepository


class ReceiptService:
    """Business logic for combining order, profile, product, and invoice data."""

    @staticmethod
    def get_receipt(order_id: str) -> Dict[str, Any]:
        # Step 1: fetch the parent order document from the orders collection.
        order = OrderRepository.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Step 2 and 3: read the user_id from the order and fetch the matching profile.
        user_id = order.get("user_id")
        profile = ProfileRepository.get_profile_by_id(user_id) if user_id else None
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found for this order")

        # Step 4 and 5: read the product_id and fetch the matching product document.
        product_id = order.get("product_id")
        product = ProductRepository.get_product_by_id(product_id) if product_id else None
        if not product:
            raise HTTPException(status_code=404, detail="Product not found for this order")

        # Step 6: find the matching invoice by order_id.
        invoice = InvoiceRepository.get_invoice_by_order_id(order_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found for this order")

        # Step 7 and 8: combine the records into a clean API response.
        receipt = {
            "order": {
                "order_id": order["_id"],
                "quantity": order["quantity"],
                "status": order["status"],
                "order_date": order["order_date"],
            },
            "customer": {
                "user_id": profile["_id"],
                "name": profile["name"],
                "email": profile["email"],
                "phone": profile["phone"],
                "address": profile["address"],
            },
            "product": {
                "product_id": product["_id"],
                "name": product["name"],
                "category": product["category"],
                "brand": product["brand"],
                "price": product["price"],
            },
            "invoice": {
                "invoice_id": invoice["_id"],
                "subtotal": invoice["subtotal"],
                "tax": invoice["tax"],
                "discount": invoice["discount"],
                "shipping": invoice["shipping"],
                "total": invoice["total"],
                "payment_status": invoice["payment_status"],
            },
        }
        return receipt

    @staticmethod
    def build_receipt(order_id: str) -> Dict[str, Any]:
        """Backward-compatible alias used by older route imports."""
        return ReceiptService.get_receipt(order_id)
