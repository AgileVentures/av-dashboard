from sqlalchemy import Column, Integer, DateTime
from datetime import datetime
from av_dashboard.our_base import Base
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
