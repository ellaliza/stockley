"""
Store management business logic.

This module contains the core business logic for store operations including
creation, member management, and data retrieval.
"""

from app.schemas.stores import *
from app.models.stores import Store
from app.models.users import StoreRoles, StoreMember, User
from app.db.session import SessionDep
from sqlmodel import Session
from app.services.users import CurrentUserDep
from app.schemas.users import StoreMemberRead, StoreMemberWrite
from app.schemas.stores import StoreReadWithProducts
from sqlmodel import select
from app.core import exceptions


def create_store(
        store_data: StoreCreate,
        session: Session,
        current_user: User
    ) -> StoreRead:
    """
    Create a new store and assign the current user as its owner.

    This function handles the complete store creation process:
    1. Creates the store record in the database
    2. Automatically creates a store membership for the current user with OWNER role
    3. Returns the store with member information

    Args:
        store_data (StoreCreate): Validated store creation data.
        session (Session): Database session for transactions.
        current_user (User): The user creating the store (becomes owner).

    Returns:
        StoreReadWithMembers: The created store with its owner member.

    Raises:
        Exception: If database operations fail.
    """
    # create the store
    db_store = Store(**store_data.model_dump())
    session.add(db_store)

    session.commit()
    session.refresh(db_store)

    # create a store member (Current user automatically owns the store)
    storemember_data = {
        "role": StoreRoles.OWNER,
        "user_id" : current_user.id,
        "store_id": db_store.id,
        "store": db_store
    }
    db_storemember = StoreMember(**storemember_data)
    session.add(db_storemember)
    session.commit()


    session.refresh(db_store)

    session.refresh(db_storemember)
    store_read = StoreReadWithMembers(**db_store.model_dump())
    return StoreReadWithMembers.model_validate(db_store)


def add_new_storemember(
        store: Store,
        new_member: User,
        current_user: User,
        session: Session,
        role: StoreRoles
):
    """
    Add a new member to an existing store with role-based authorization.

    This function performs several checks before adding a member:
    1. Verifies that the current user is an owner of the store
    2. Checks that the new member is not already part of the store
    3. Creates the membership record with the specified role

    Args:
        store (Store): The store to add the member to (with members relationship loaded).
        new_member (User): The user to add as a member.
        current_user (User): The user performing the action (must be store owner).
        session (Session): Database session for transactions.
        role (StoreRoles): The role to assign to the new member (OWNER or STAFF).

    Returns:
        StoreReadWithMembers: The updated store with the new member included.

    Raises:
        UnauthorizedError: If the current user is not a store owner.
        UserAlreadyAssignedToStore: If the user is already a member of the store.
    """
    is_owner = any(
        m.user_id == current_user.id and m.role == StoreRoles.OWNER
        for m in store.members
    )
    if not is_owner:
        raise exceptions.UnauthorizedError(
            "Only store owners can add members"
        )

    already_member = any(
        m.user_id == new_member.id
        for m in store.members
    )

    if already_member:
        raise exceptions.UserAlreadyAssignedToStore(
            f"User {new_member.username} is already a member"
        )

    storemember_data = {
        "role": role,
        "user_id" : new_member.id,
        "store_id": store.id,

    }
    db_storemember = StoreMember(**storemember_data)
    session.add(db_storemember)
    session.commit()

    session.refresh(db_storemember)
    session.refresh(store)
    return StoreReadWithMembers.model_validate(store)


def get_stores(session: Session) -> list[StoreReadWithMembers]:
    """
    Retrieve all stores with their member information.

    This function performs a complex join query to fetch stores along with
    their members and user details in a single database query. The results
    are then grouped by store and formatted into the appropriate response schema.

    Args:
        session (Session): Database session for querying.

    Returns:
        List[StoreReadWithMembers]: List of all stores with complete member information.

    Note:
        This function uses a manual grouping approach because SQLModel's
        relationship loading doesn't handle the complex member aggregation well.
    """
    stmt = (
        select(Store, User, StoreMember)
        .join(StoreMember, StoreMember.store_id == Store.id)
        .join(User, User.id == StoreMember.user_id)
    )

    rows = session.exec(stmt).all()

    stores_map: dict[int, dict] = {}

    for store, user, membership in rows:
        if store.id not in stores_map:
            stores_map[store.id] = {
                "id": store.id,
                "name": store.name,
                "description": store.description,
                "location": store.location,
                "members": []
            }

        stores_map[store.id]["members"].append({
            "id": membership.id,
            "role": membership.role,
            "created_at": membership.created_at,
            "user": user,
            "user_id": membership.user_id
        })

    return [
        StoreReadWithMembers.model_validate(store_data)
        for store_data in stores_map.values()
    ]


def get_store(session: Session, store_id: int) -> Store:
    """
    Retrieve a single store by its ID.

    Args:
        session (Session): Database session for querying.
        store_id (int): The unique identifier of the store.

    Returns:
        Store: The store object if found, None otherwise.
    """
    stmt = select(Store).where(Store.id == store_id)
    store = session.exec(stmt).first()
    return store


def get_store_with_products(session: Session, store_id: int, current_user: User) -> StoreReadWithProducts | None:
    """
    Retrieve a single store by its ID.

    Args:
        session (Session): Database session for querying.
        store_id (int): The unique identifier of the store.

    Returns:
        Store: The store object if found, None otherwise.
    """
    stmt = select(Store).where(Store.id == store_id)
    store = session.exec(stmt).first()
    for membership in current_user.store_memberships:
        if membership.store_id == store_id:
            return StoreReadWithProducts.model_validate(store)
        else:
            return None

