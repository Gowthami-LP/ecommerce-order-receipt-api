from typing import List

from fastapi import APIRouter, HTTPException, status

from app.repositories.profile_repository import ProfileRepository
from app.schemas.profile import ProfileCreate, ProfileResponse, ProfileUpdate

router = APIRouter(prefix="/api/profiles", tags=["Profiles"])


@router.post("", response_model=ProfileResponse, summary="Create a profile")
def create_profile(profile: ProfileCreate):
    """Create a customer profile in the profiles collection."""
    if ProfileRepository.get_profile_by_id(profile.user_id):
        raise HTTPException(status_code=400, detail="Profile already exists")

    profile_data = {
        "_id": profile.user_id,
        "name": profile.name,
        "email": profile.email,
        "phone": profile.phone,
        "address": profile.address.model_dump(),
    }
    ProfileRepository.create_profile(profile_data)
    return ProfileResponse(
        user_id=profile_data["_id"],
        name=profile_data["name"],
        email=profile_data["email"],
        phone=profile_data["phone"],
        address=profile_data["address"],
    )


@router.get("/{user_id}", response_model=ProfileResponse, summary="Get a profile")
def get_profile(user_id: str):
    """Fetch one profile using the user ID."""
    profile = ProfileRepository.get_profile_by_id(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return ProfileResponse(**profile)


@router.get("", response_model=List[ProfileResponse], summary="List all profiles")
def list_profiles():
    """Return all customer profiles."""
    return [ProfileResponse(**profile) for profile in ProfileRepository.get_all_profiles()]


@router.put("/{user_id}", response_model=ProfileResponse, summary="Update a profile")
def update_profile(user_id: str, profile: ProfileUpdate):
    """Update the selected profile using a partial payload."""
    existing = ProfileRepository.get_profile_by_id(user_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Profile not found")

    update_data = profile.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No profile fields provided for update")

    if "address" in update_data:
        update_data["address"] = update_data["address"].model_dump()

    ProfileRepository.update_profile(user_id, update_data)
    updated = ProfileRepository.get_profile_by_id(user_id)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update profile")
    return ProfileResponse(**updated)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK, summary="Delete a profile")
def delete_profile(user_id: str):
    """Delete a profile by user ID."""
    existing = ProfileRepository.get_profile_by_id(user_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Profile not found")

    ProfileRepository.delete_profile(user_id)
    return {"message": "Profile deleted successfully"}
