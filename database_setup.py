from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import random
import string
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)

Base = declarative_base()

# generate random key for hashing
sKey = "".join(random.choice(string.ascii_uppercase +
                             string.digits) for x in xrange(32))


# category table
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    items = relationship("Item")

    # jsonify function
    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'item': [i.serialize for i in self.items],
        }


# item table
class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    cat_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category, back_populates="items")
    title = Column(String)
    desc = Column(String)
    creator_id = Column(String, ForeignKey('user.id'))
    creator_email = Column(String, ForeignKey('user.email'))

    # jsonify function
    @property
    def serialize(self):
        return{
            'id': self.id,
            'cat_id': self.cat_id,
            'title': self.title,
            'desc': self.desc,
            'creator': self.creator_email
        }


# user table
class User(Base):
    __tablename__ = 'user'
    # id will be google auth 'sub' var
    id = Column(String, primary_key=True)
    email = Column(String, nullable=False)

    def gen_auth_token(self, expiration=3600):
        s = Serializer(sKey, expires_in=expiration)
        return s.dumps({'id': self.id})

    # token verification function
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(sKey)
        try:
            d = s.loads(token)
        # expired token
        except SignatureExpired:
            return None
        # invalid token
        except BadSignature:
            return None
        user_id = d['id']
        return user_id

    # jsonify function
    @property
    def serialize(self):
        return{
            'id': self.id,
            'email': self.email,
            'pic': self.pic
        }


engine = create_engine('postgresql://catalog:123password@localhost/itemCatalog')

Base.metadata.create_all(engine)
