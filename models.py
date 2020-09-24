from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text, Date
from settings import engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Campaign(Base):
    __tablename__ = 'campaign'
    id = Column(Integer, primary_key=True, autoincrement=True)
    campaign_name = Column(String(50))
    amount_contributed = Column(Integer, default=0)
    user_email = Column(String(50))
 

Base.metadata.create_all(engine)