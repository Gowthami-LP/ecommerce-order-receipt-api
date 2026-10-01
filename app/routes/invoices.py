from typing import List

from fastapi import APIRouter, HTTPException, status

from app.repositories.invoice_repository import InvoiceRepository
from app.schemas.invoice import InvoiceCreate, InvoiceResponse, InvoiceUpdate

router = APIRouter(prefix="/api/invoices", tags=["Invoices"])


@router.post("", response_model=InvoiceResponse, summary="Create an invoice")
def create_invoice(invoice: InvoiceCreate):
    """Create an invoice associated with an order."""
    if InvoiceRepository.get_invoice_by_id(invoice.invoice_id):
        raise HTTPException(status_code=400, detail="Invoice already exists")

    invoice_data = {
        "_id": invoice.invoice_id,
        "order_id": invoice.order_id,
        "subtotal": invoice.subtotal,
        "tax": invoice.tax,
        "discount": invoice.discount,
        "shipping": invoice.shipping,
        "total": invoice.total,
        "payment_status": invoice.payment_status,
    }
    InvoiceRepository.create_invoice(invoice_data)
    return InvoiceResponse(
        invoice_id=invoice_data["_id"],
        order_id=invoice_data["order_id"],
        subtotal=invoice_data["subtotal"],
        tax=invoice_data["tax"],
        discount=invoice_data["discount"],
        shipping=invoice_data["shipping"],
        total=invoice_data["total"],
        payment_status=invoice_data["payment_status"],
    )


@router.get("/{invoice_id}", response_model=InvoiceResponse, summary="Get an invoice")
def get_invoice(invoice_id: str):
    """Fetch an invoice by its ID."""
    invoice = InvoiceRepository.get_invoice_by_id(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return InvoiceResponse(**invoice)


@router.get("", response_model=List[InvoiceResponse], summary="List all invoices")
def list_invoices():
    """Return all invoices in the invoices collection."""
    return [InvoiceResponse(**invoice) for invoice in InvoiceRepository.get_all_invoices()]


@router.put("/{invoice_id}", response_model=InvoiceResponse, summary="Update an invoice")
def update_invoice(invoice_id: str, invoice: InvoiceUpdate):
    """Update details of an invoice."""
    existing = InvoiceRepository.get_invoice_by_id(invoice_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Invoice not found")

    update_data = invoice.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No invoice fields provided for update")

    InvoiceRepository.update_invoice(invoice_id, update_data)
    updated = InvoiceRepository.get_invoice_by_id(invoice_id)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update invoice")
    return InvoiceResponse(**updated)


@router.delete("/{invoice_id}", status_code=status.HTTP_200_OK, summary="Delete an invoice")
def delete_invoice(invoice_id: str):
    """Delete an invoice by ID."""
    existing = InvoiceRepository.get_invoice_by_id(invoice_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Invoice not found")

    InvoiceRepository.delete_invoice(invoice_id)
    return {"message": "Invoice deleted successfully"}
