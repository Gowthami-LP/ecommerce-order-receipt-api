from fastapi import APIRouter

from app.schemas.receipt import ReceiptResponse
from app.services.receipt_service import ReceiptService

router = APIRouter(prefix="/api", tags=["Receipts"])


@router.get(
    "/orders/{order_id}/receipt",
    response_model=ReceiptResponse,
    summary="Get complete order receipt",
    description="Returns order, customer, product, and invoice information by combining data from multiple MongoDB collections.",
)
def get_order_receipt(order_id: str):
    """Build a complete receipt by joining profile, product, order and invoice data."""
    return ReceiptService.get_receipt(order_id)
