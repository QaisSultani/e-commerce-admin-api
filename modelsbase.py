from datetime import datetime
from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=100, max_length=1000)
    price: float = Field(gt=0)
    remaining_stock: int = Field(default=0, gt=-1)
    # created_at: datetime | None = None
    # remaining_stock: int = Field(gt=0)
    # total_sale_qty: int = Field(gt=0)
    # total_sale_amount: float = Field(gt=0)
    # user_id: int

# class InventoryBase(BaseModel):
#     product_id: int
#     remaining_stock: int = Field(default=0, gt=-1)
#     total_sale_qty: int = Field(default=0, gt=-1)
#     total_sale_amount: float = Field(default=0)
#     low_stock: bool = Field(default=True)
#     # created_at: datetime | None = None

class UpdateStockBase(BaseModel):
    remaining_stock: int = Field(gt=-1)