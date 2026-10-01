from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.database.mongodb import get_collection


class ProfileRepository:
    """Database access for the profiles collection."""

    collection = get_collection("profiles")

    @staticmethod
    def create_profile(data: Dict[str, Any]) -> Dict[str, Any]:
        ProfileRepository.collection.insert_one(data)
        return data

    @staticmethod
    def get_profile_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        return ProfileRepository.collection.find_one({"_id": user_id})

    @staticmethod
    def get_all_profiles() -> List[Dict[str, Any]]:
        return list(ProfileRepository.collection.find())

    @staticmethod
    def update_profile(user_id: str, data: Dict[str, Any]) -> bool:
        result = ProfileRepository.collection.update_one({"_id": user_id}, {"$set": data})
        return result.modified_count > 0

    @staticmethod
    def delete_profile(user_id: str) -> bool:
        result = ProfileRepository.collection.delete_one({"_id": user_id})
        return result.deleted_count > 0
