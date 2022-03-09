from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from db_config import Base


class Customer(Base):
    __tablename__ = 'customers'

    cust_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    address = Column(String(50), nullable=False)

    @property
    def serialize(self):
        data = {'cust_id': self.cust_id, 'name': self.name, 'address': self.address}
        return data


# class Customer:
#     def __init__(self, cust_id, name, address):
#         self.cust_id = cust_id
#         self.name = name
#         self.address = address
#
#     @property
#     def serialize(self):
#         data = {'cust_id': self.cust_id, 'name': self.name, 'address': self.address}
#         return data
