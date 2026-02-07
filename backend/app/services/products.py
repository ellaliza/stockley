from sqlmodel import Session, select
from app.models.products import Product, StockMovement
from app.schemas.products import ProductBase, ProductRead, StockMovementCreate, StockMovementTypes, ProductUpdate
from app.models.users import User
from typing import Optional, List, Union


def add_product_to_store(session: Session, product: ProductBase, store_id: int) -> ProductRead:
    """Create a new `Product` row and add an initial stock movement.

    - `product` is a validated `ProductBase` instance (typically
      constructed from the request body).
    - `store_id` is included to ensure the product is associated with
      the correct store. The function returns a `ProductRead` schema
      (Pydantic model) for API serialization.

    Note: This function persists both the `Product` and an initial
    `StockMovement` entry that records the initial stock as a
    `StockMovementTypes.IN` event.
    """

    # Convert Pydantic model to plain dict (this uses field names)
    product_data = product.model_dump()

    # Persist the product
    db_product = Product(**product_data)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    # Record the initial stock as a stock movement for audit/history
    stock_data = {
        "movement_type": StockMovementTypes.IN,
        "product_id": db_product.product_id,
        "quantity": db_product.current_stock,
        "note": f"Initial Stock of {db_product.product_name}",
    }
    stock_movement = StockMovement(**stock_data)
    session.add(stock_movement)
    session.commit()

    # Return a validated read model for consistency with API responses
    return ProductRead.model_validate(db_product)


def get_products_from_store(session: Session, store_id: int, product_id: Optional[int] = None) -> Union[Product, List[Product], None]:
    """Retrieve products for a store.

    - If `product_id` is provided, returns a single `Product` or None.
    - Otherwise returns a list of `Product` instances for the store.
    """

    if product_id is not None:
        stmt = select(Product).where(Product.store_id == store_id, Product.product_id == product_id)
        product = session.exec(stmt).first()
        return product
    else:
        stmt = select(Product).where(Product.store_id == store_id)
        products = session.exec(stmt).all()
        return products


def update_product(session: Session, product: ProductUpdate) -> Optional[Product]:
    """Apply an update to a product and persist it.

    - `product` should be a `ProductUpdate` instance. Only fields that
      are set (use `exclude_unset=True` when generating `dict`) will be
      applied to the DB model. Returns the updated `Product` or None
      if the product was not found.

    Note: This function performs a straightforward attribute copy and
    does not currently create StockMovement records for quantity
    changes. If auditing of stock changes is required, create
    StockMovement entries at the call site (API layer) or extend this
    service to accept an optional movement record.
    """

    db_product = session.get(Product, product.product_id)

    if not db_product:
        return None

    # Only update attributes that were provided by the caller
    data = product.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(db_product, key, value)

    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    return db_product
