from sqlalchemy import Column, Integer
from av_dashboard.our_base import Base
class Plan(Base):
    __tablename__ = 'plans'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
