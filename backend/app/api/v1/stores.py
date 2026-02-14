"""
Store management API endpoints.

This module provides REST API endpoints for managing stores in the inventory system.
Stores can be created, listed, and members can be added with role-based permissions.
"""

from fastapi import APIRouter, HTTPException, status, Response
from app.db.session import SessionDep
from app.services.stores import create_store, get_stores, add_new_storemember, get_store, get_store_with_products, delete_a_store
from app.services.users import CurrentUserDep
from app.schemas.stores import StoreReadWithMembers, StoreCreate, StoreReadWithProducts
from app.core import exceptions
from app.models.users import StoreRoles
from app.services.auth import get_user_by_email, get_user_by_username

router = APIRouter(prefix="/stores", tags=["Stores"])


@router.post("/")
async def create_new_store(store_data: StoreCreate, session: SessionDep, current_user: CurrentUserDep):
    """
    Create a new store.

    This endpoint allows authenticated users to create a new store. The current user
    automatically becomes the owner of the newly created store.

    Args:
        store_data (StoreCreate): The store creation data containing name, description, and location.
        session (SessionDep): Database session dependency.
        current_user (CurrentUserDep): The currently authenticated user.

    Returns:
        StoreReadWithMembers: The created store with its initial owner member.

    Raises:
        HTTPException: If store creation fails due to validation or database errors.
    """
    try:
        store = create_store(store_data, session, current_user)
        return store
    except Exception as e:
        return HTTPException(status.HTTP_400_BAD_REQUEST, f"An error occured: {str(e)}")


@router.get("/")
async def get_all_stores(session: SessionDep, current_user: CurrentUserDep):
    """
    Retrieve all stores.

    This endpoint returns a list of all stores in the system, including their members.
    Requires authentication but no specific permissions.

    Args:
        session (SessionDep): Database session dependency.
        current_user (CurrentUserDep): The currently authenticated user (for auth check).

    Returns:
        List[StoreReadWithMembers]: List of all stores with their member information.

    Raises:
        HTTPException: If retrieval fails due to database errors.
    """
    try:
        stores = get_stores(session)
        return stores
    except Exception as e:
        return HTTPException(status.HTTP_400_BAD_REQUEST, f"An error occured: {str(e)}")

@router.get("/{store_id}", response_model=StoreReadWithProducts | None)
async def get_store(session: SessionDep, current_user: CurrentUserDep, store_id : int):
    """
    Retrieve a specific store by ID with its products.

    This endpoint returns a store and all of its associated products.
    Requires authentication but no specific permissions.

    Args:
        session (SessionDep): Database session dependency.
        current_user (CurrentUserDep): The currently authenticated user (for auth check).
        store_id (int): The ID of the store to retrieve.

    Returns:
        StoreReadWithProducts | None: The store with its products, or None if not found.

    Raises:
        HTTPException: If retrieval fails due to database errors.
    """
    try:
        store = get_store_with_products(session, store_id, current_user)
        return store
    except Exception as e:
        return HTTPException(status.HTTP_400_BAD_REQUEST, f"An error occured: {str(e)}")

@router.delete("/{store_id}")
async def delete_store(session: SessionDep, current_user: CurrentUserDep, store_id : int):
    """
    Delete a store. Only the store owner can delete it.

    This endpoint allows store owners to delete their stores.
    All associated data (products, members) will be removed.

    Args:
        session (SessionDep): Database session dependency.
        current_user (CurrentUserDep): The currently authenticated user (must be store owner).
        store_id (int): The ID of the store to delete.

    Returns:
        dict: Confirmation message with success status.

    Raises:
        HTTPException: If deletion fails due to permission issues or database errors.
    """
    try:
        delete_a_store(session, store_id, user_id = current_user.id)
        
        return {"success": True, "message": "Store Deleted"}
    except Exception as e:
        return HTTPException(status.HTTP_400_BAD_REQUEST, f"An error occured: {str(e)}")

@router.post("/add-member")
async def add_a_new_storemember(
    session: SessionDep,
    current_user: CurrentUserDep,
    store_id: int,
    new_member_email: str | None = None,
    new_member_username: str | None = None,
    role: StoreRoles = StoreRoles.STAFF
):
    """
    Add a new member to an existing store.

    This endpoint allows store owners to add new members to their stores.
    The new member can be specified by email or username, and assigned a role.
    Only store owners can perform this action.

    Args:
        session (SessionDep): Database session dependency.
        current_user (CurrentUserDep): The currently authenticated user (must be store owner).
        store_id (int): The ID of the store to add the member to.
        new_member_email (str | None): Email of the user to add (alternative to username).
        new_member_username (str | None): Username of the user to add (alternative to email).
        role (StoreRoles): The role to assign to the new member (OWNER or STAFF). Defaults to STAFF.

    Returns:
        StoreReadWithMembers: The updated store with the new member included.

    Raises:
        HTTPException: If the operation fails due to permission issues, user not found, or database errors.
    """
    try:
        if not new_member_email and not new_member_username:
            return exceptions.bad_request_exception("Please provide the email or username of the new member")
        if new_member_email:
            new_member = get_user_by_email(session, new_member_email)
        elif new_member_username:
            new_member = get_user_by_username(session, new_member_username)

        store = get_store(session=session, store_id=store_id)

        updated_store = add_new_storemember(store, new_member, current_user, session, role)
        return updated_store
    except Exception as e:
        return exceptions.bad_request_exception(f"{str(e)}")