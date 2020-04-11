from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB_setup_alchemy import Base,User,Visitor,VisitRecord
from os import getcwd

# link to the DB we are using
# pay attention to this part, if without check_same_thread=false, there will be lots of errors
# but what is going on behind this part of code
# what does engine and session really means
def main():
    db_path='sqlite:///'+getcwd()+'/data.db'
    engine = create_engine(db_path,connect_args={'check_same_thread': False})
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    """ try:
        new_user=User(name="testname",email="test_email")
        session.add(new_user)
        session.commit()
        print("new user created")
    except:
        print("this user is already in the database") """
    
    test_user=session.query(User).filter_by(name="testname").one()
    print(test_user.name,test_user.email)


if __name__=="__main__":
    main()
