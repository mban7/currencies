from db import Base
from sqlalchemy import Column, DateTime, Float, Integer, String


class Currency(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, index=True)
    mid = Column(Float, index=True)
    date = Column(DateTime, index=True)
