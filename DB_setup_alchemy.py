from sqlalchemy import Column, ForeignKey, Integer, String, LargeBinary
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
    name = Column(String(250), nullable = False)
    photo=Column(LargeBinary,nullable=False)
    user_name=Column(Integer,ForeignKey('user.name'))
    user = relationship(User)

class VisitRecord(Base):
    __tablename__="visit_record"

    # use id as primary key
    record_id=Column(Integer,primary_key=True)
    date=Column(String(250),nullable=False)
    user_name=Column(String(250),ForeignKey('user.name'))
    user=relationship(User)
    visitor_id=Column(Integer,ForeignKey('visitor.visitor_id'),nullable=True)
    # if not permitted visitor, lable as stranger
    visitor_name=Column(String(250),nullable=False)
    visitor=relationship(Visitor)

def main():
    # link to the DB we are using
    engine = create_engine('sqlite:///data.db')

    Base.metadata.create_all(engine)

if __name__=="__main__":
    main()
