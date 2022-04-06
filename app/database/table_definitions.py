# Third-party imports
from sqlalchemy import MetaData, Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


meta = MetaData()
Base = declarative_base()


class customers(Base):
    __tablename__ = 'customers'
    customer_id = Column(String, primary_key=True, nullable=False)
    loc_id = Column(Integer, ForeignKey("locations.loc_id"), nullable=False)


class suppliers(Base):
    __tablename__ = 'suppliers'
    supp_id = Column(String, primary_key=True, nullable=False)
    loc_id = Column(Integer, ForeignKey("locations.loc_id"), nullable=False)


class locations(Base):
    __tablename__ = 'locations'
    loc_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    loc_name = Column(String, nullable=False, unique=True)


class orders(Base):
    __tablename__ = 'orders'
    order_id = Column(String, primary_key=True)
    customer_id = Column(ForeignKey("customers.customer_id"), nullable=False)
    supp_id = Column(ForeignKey("suppliers.supp_id"), nullable=False)
    date = Column(DateTime)
    req_amount = Column(Float)
    supp_amount = Column(Float)
    cost = Column(Float)


def create_tables(engine):
    Base.metadata.create_all(engine)
