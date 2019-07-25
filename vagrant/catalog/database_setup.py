from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()

class Item(Base):
    __tablename__ = 'item'


engine = create_engine('sqlite:///itemCatalog.db')
 
Base.metadata.create_all(engine)