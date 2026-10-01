from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.database.mongodb import get_collection


class OrderRepository:
    """Database access for the orders collection."""

    collection = get_collection("orders")

    @staticmethod
    def create_order(data: Dict[str, Any]) -> Dict[str, Any]:
        OrderRepository.collection.insert_one(data)
        return data

    @staticmethod
    def get_order_by_id(order_id: str) -> Optional[Dict[str, Any]]:
        return OrderRepository.collection.find_one({"_id": order_id})

    @staticmethod
    def get_all_orders() -> List[Dict[str, Any]]:
        return list(OrderRepository.collection.find())

    @staticmethod
    def update_order(order_id: str, data: Dict[str, Any]) -> bool:
        result = OrderRepository.collection.update_one({"_id": order_id}, {"$set": data})
        return result.modified_count > 0

    @staticmethod
    def delete_order(order_id: str) -> bool:
        result = OrderRepository.collection.delete_one({"_id": order_id})
        return result.deleted_count > 0
