import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String,LargeBinary
# import this declarative base to inherate
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class User(Base):
    # this var refers to a table in database
    __tablename__ = 'user'

    # name is primary key, which means each user must has a unique name
    name = Column(String(250), nullable=False,primary_key=True)
    email=Column(String(250),nullable=False)
 
class Visitor(Base):
    __tablename__ = 'visitor'

    visitor_id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    photo=Column(LargeBinary,nullable=False)
    user_name=Column(Integer,ForeignKey('user.name'))
    user = relationship(User)

#We added this serialize function to be able to send JSON objects in a serializable format
    """ @property
    def serialize(self):
       
        return {
            'name'         : self.name,
            'description'         : self.description,
            'id'         : self.id,
            'price'         : self.price,
            'course'         : self.course,
        } """
 
# link to the DB we are using
engine = create_engine('sqlite:///data.db')

Base.metadata.create_all(engine)