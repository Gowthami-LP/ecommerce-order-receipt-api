from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.database.mongodb import get_collection


class InvoiceRepository:
    """Database access for the invoices collection."""

    collection = get_collection("invoices")

    @staticmethod
    def create_invoice(data: Dict[str, Any]) -> Dict[str, Any]:
        InvoiceRepository.collection.insert_one(data)
        return data

    @staticmethod
    def get_invoice_by_id(invoice_id: str) -> Optional[Dict[str, Any]]:
        return InvoiceRepository.collection.find_one({"_id": invoice_id})

    @staticmethod
    def get_invoice_by_order_id(order_id: str) -> Optional[Dict[str, Any]]:
        return InvoiceRepository.collection.find_one({"order_id": order_id})

    @staticmethod
    def get_all_invoices() -> List[Dict[str, Any]]:
        return list(InvoiceRepository.collection.find())

    @staticmethod
    def update_invoice(invoice_id: str, data: Dict[str, Any]) -> bool:
        result = InvoiceRepository.collection.update_one({"_id": invoice_id}, {"$set": data})
        return result.modified_count > 0

    @staticmethod
    def delete_invoice(invoice_id: str) -> bool:
        result = InvoiceRepository.collection.delete_one({"_id": invoice_id})
        return result.deleted_count > 0
