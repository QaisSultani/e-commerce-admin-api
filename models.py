from sqlalchemy import Boolean, Column, Integer, String, Float
from database import Base

class Inventory(Base):
    __tablename__ = 'inventories'
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100), index=True)
    product_description = Column(String(1000))
    price = Column(Float)
    remaining_stock = Column(Integer)
    total_sale_qty = Column(Integer)
    total_sale_amount = Column(Float)
    user_id = Column(Integer)
