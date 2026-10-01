from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.database.mongodb import get_collection


class ProductRepository:
    """Database access for the products collection."""

    collection = get_collection("products")

    @staticmethod
    def create_product(data: Dict[str, Any]) -> Dict[str, Any]:
        ProductRepository.collection.insert_one(data)
        return data

    @staticmethod
    def get_product_by_id(product_id: str) -> Optional[Dict[str, Any]]:
        return ProductRepository.collection.find_one({"_id": product_id})

    @staticmethod
    def get_all_products() -> List[Dict[str, Any]]:
        return list(ProductRepository.collection.find())

    @staticmethod
    def update_product(product_id: str, data: Dict[str, Any]) -> bool:
        result = ProductRepository.collection.update_one({"_id": product_id}, {"$set": data})
        return result.modified_count > 0

    @staticmethod
    def delete_product(product_id: str) -> bool:
        result = ProductRepository.collection.delete_one({"_id": product_id})
        return result.deleted_count > 0
