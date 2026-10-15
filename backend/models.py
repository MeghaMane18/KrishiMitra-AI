from sqlalchemy import Column, Integer, String, Float
from .database import Base


class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    farmer_name = Column(String, nullable=False)
    farm_name = Column(String, nullable=False)
    location = Column(String)
    total_acres = Column(Float)

class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String, nullable=False)
    area_acres = Column(Float)
    sowing_date = Column(String)
    season = Column(String)
    farm_id = Column(Integer)
    
class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    animal_name = Column(String, nullable=False)
    animal_type = Column(String)
    breed = Column(String)
    age = Column(Float)
    farm_id = Column(Integer)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    category = Column(String)
    price = Column(Float)
    stock_quantity = Column(Float)

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    quantity = Column(Float)
    total_amount = Column(Float)
    customer_name = Column(String)
    sale_date = Column(String)
    amount_paid = Column(Float, default=0)
    remaining_balance = Column(Float, default=0)


class MilkRecord(Base):
    __tablename__ = "milk_records"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer)
    milk_date = Column(String)
    morning_milk = Column(Float)
    evening_milk = Column(Float)
    total_milk = Column(Float)

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    worker_name = Column(String, nullable=False)
    phone = Column(String)
    work_type = Column(String)
    work_date = Column(String)
    days_worked = Column(Float)
    rate_per_day = Column(Float)
    total_payment = Column(Float)
    payment_status = Column(String)
    advance_payment = Column(Float, default=0)
    remaining_payment = Column(Float, default=0)
    

class FarmTransaction(Base):
    __tablename__ = "farm_transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(String, nullable=False)
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String)
    transaction_date = Column(String, nullable=False)

