from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from database import Base

class Customer(Base):
    __tablename__ = 'customer'

    customerID = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone_no = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    username = Column(String)

    accounts = relationship('Account', back_populates='customer')

class Account(Base):
    __tablename__ = 'account'

    AccountID = Column(Integer, primary_key=True, index=True)
    CustomerID = Column(Integer, ForeignKey('customer.customerID'))
    type = Column(String)
    Balance = Column(Numeric(10,2))

    customer = relationship('Customer', back_populates='accounts')
    transactions = relationship('Transaction', back_populates='account')

class Transaction(Base):
    __tablename__ = 'transaction'

    TransactionID = Column(String, primary_key=True, index=True)
    AccountID = Column(Integer, ForeignKey('account.AccountID'))
    type = Column(String)
    Amount = Column(Float)
    Timestamp = Column(DateTime)

    account = relationship('Account', back_populates='transactions')
