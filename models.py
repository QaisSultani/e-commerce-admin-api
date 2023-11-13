from datetime import datetime
from itertools import product
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True)
    email = Column(String(50), nullable=False, unique=True, index=True)

    orders = relationship('Order', back_populates='user')

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(1000), nullable=False)
    price = Column(Float, nullable=False)
    remaining_stock = Column(Integer, nullable=False, default=0)
    total_sale_qty = Column(Integer, nullable=False, default=0)
    total_sale_amount = Column(Float, nullable=False, default=0)
    low_stock = Column(Boolean, nullable=False, default=True)

    orders = relationship('Order', back_populates='product')

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Order(Base):
    __tablename__ = 'orders'

    id  = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    qty = Column(Integer, nullable=False)

    user = relationship('User', back_populates='orders')
    product = relationship('Product', back_populates='orders')
    # product_id = Column()

# class Inventory(Base):
#     __tablename__ = 'inventories'
    
#     id = Column(Integer, primary_key=True, index=True)
#     product_id = Column(Integer, unique=True)
#     remaining_stock = Column(Integer, nullable=False, default=0)
#     total_sale_qty = Column(Integer, nullable=False, default=0)
#     total_sale_amount = Column(Float, nullable=False, default=0)
#     low_stock = Column(Boolean, nullable=False, default=True)
#     # created_at = Column(DateTime, default=datetime.utcnow, server_default='CURRENT_TIMESTAMP')

#     def as_dict(self):
#        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

