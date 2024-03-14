from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import validates

from app import db


class Products(db.Model):
    # __tablename__ = 'Products'
    id = Column(Integer, primary_key = True)
    name = Column(String(50))
    category = Column(String(50))
    brand = Column(String(50))
    qty = Column(Integer)
    price = Column(Integer)
    def __str__(self):
        return self.name