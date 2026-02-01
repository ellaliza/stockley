from app.schemas.stores import *

def create_store(store_data: dict) -> StoreRead:
    store = StoreCreate(**store_data)