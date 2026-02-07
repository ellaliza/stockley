from fastapi import APIRouter, HTTPException, Query, status
from app.schemas.products import ProductRead, ProductUpdate, ProductBase, ProductCreate, ProductBulkCreate
from sqlmodel import select, Session
from app.models.products import Product
from app.db.session import SessionDep
from app.services.users import CurrentUserDep, is_user_in_store
from app.services.stores import get_store
from app.services.products import *
from app.core.exceptions import StoreNotFoundError, UnauthorizedError

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

@router.get("/{store_id}/{product_id}", response_model=ProductRead, response_model_by_alias=True)
async def get_product(session: SessionDep, current_user: CurrentUserDep, product_id: int, store_id: int):
    user_is_member = is_user_in_store(session, current_user.id, store_id)
    if not user_is_member:
        return HTTPException(status_code=401, detail="Not permitted to access the requested resource")
    product = get_products_from_store(session, store_id, product_id=product_id)
    
    return ProductRead.model_validate(product)

@router.get("/{store_id}", response_model=list[ProductRead])
async def get_products(session: SessionDep, current_user: CurrentUserDep, store_id: int):
    user_is_member = is_user_in_store(session, current_user.id, store_id)

    if not user_is_member:
        return HTTPException(status_code=401, detail="Not permitted to access the requested resource")
    products = get_products_from_store(session, store_id)
    print(len(list(products)))
    return [ProductRead.model_validate(product) for product in products]
    
@router.post("/", response_model=ProductRead)
async def create_product(product: ProductCreate, session: SessionDep, current_user: CurrentUserDep):
    raw_product = ProductBase.model_validate(product)
    user_is_member = is_user_in_store(session, current_user.id, product.store_id)
    
    if not user_is_member:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to add products to this store"
        )
    prod = add_product_to_store(session, raw_product, product.store_id)
    return prod


@router.post("/bulk-create/", response_model=list[ProductRead])
async def create_bulk_products(product_list: ProductBulkCreate, session: SessionDep, current_user: CurrentUserDep):
    """Create multiple products in a single request for a given store.

    Authorization: caller must be a member of the target store.
    """
    # Use the store id provided with the bulk payload for the membership check
    user_is_member = is_user_in_store(session, current_user.id, product_list.store_id)

    if not user_is_member:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to add products to this store",
        )

    products: list[ProductRead] = []
    for product in product_list.products:
        raw_product = ProductBase.model_validate(product)

        prod = add_product_to_store(session, raw_product, product_list.store_id)
        products.append(prod)

    return products

@router.post("/stock-out/{store_id}/{product_id}", response_model=ProductRead)
async def sell_product(
    store_id: int,
    product_id: int,
    session: SessionDep,
    current_user: CurrentUserDep,
    quantity: int = Query(default=1, ge=1),
):
    """Decrease a product's stock by `quantity` (sell operation).

    Requires the caller to be a member of the store.
    """
    product: Product = get_products_from_store(session, store_id, product_id)
    # Authorization: ensure the caller is a member of the store
    user_is_member = is_user_in_store(session, current_user.id, store_id)
    if not user_is_member:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.current_stock < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # Reduce available stock and persist the change. Stock movement
    # auditing can be added in the service layer if required.
    product.current_stock -= quantity
    data = product.model_dump()
    data["store_id"] = store_id

    new_product = ProductUpdate(**data)

    updated_product = update_product(session, new_product)

    return ProductRead.model_validate(updated_product)


@router.post("/stock-in/{store_id}/{product_id}", response_model=ProductRead)
async def restock_product(
    store_id: int,
    product_id: int,
    session: SessionDep,
    current_user: CurrentUserDep,
    quantity: int = Query(default=1, ge=1),
):
    """Increase a product's stock by `quantity` (restock operation).

    Requires the caller to be a member of the store. Previously the
    logic incorrectly subtracted stock; this endpoint now increments
    `current_stock` by `quantity`.
    """

    # Authorization: ensure the caller is a member of the store
    user_is_member = is_user_in_store(session, current_user.id, store_id)
    if not user_is_member:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

    product: Product = get_products_from_store(session, store_id, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Increase stock by requested quantity and persist
    product.current_stock += quantity
    data = product.model_dump()
    data["store_id"] = store_id

    new_product = ProductUpdate.model_validate(product)
    updated_product = update_product(session, new_product)

    return ProductRead.model_validate(updated_product)

""" 
@router.get("/api/dashboard", response_model=DashboardData)
async def get_dashboard_data(session: SessionDep):
    products = session.exec(select(Product)).all()

    total_product_count = len(products)
    low_stock_count = sum(
        1 for product in products
        if product.current_stock < product.minimum_stock_level
    )
    out_of_stock_count = sum(
        1 for product in products
        if product.current_stock == 0
    )

    return DashboardData(
        total_product_count=total_product_count,
        low_stock_count=low_stock_count,
        out_of_stock_count=out_of_stock_count
    ) """