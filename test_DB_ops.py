import cv2
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB_setup_alchemy import Base, User, Visitor
import DB_ops
from AWS_API import is_match

engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

""" def show_img(img):
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows() """

def add_new_visitor(user_name,visitor_name,photo_path):
    try:
        photo=open(photo_path,'rb').read()
        DB_ops.add_new_visitor(user_name,visitor_name,photo,session)
    except:
        print("photo not found in %s" % photo_path)

def img_full_path(folder_name,file_name):
    return os.getcwd()+os.sep+folder_name+os.sep+file_name

def init_DB():
    user_name="bob"
    email="xxxxxxxxxxxxxxxxxx"
    name_lis=["gates","musk","donald"]
    folder_name="imgs"
    DB_ops.create_new_user(user_name,email,session)
    for name in name_lis:
        add_new_visitor(user_name,name,img_full_path(folder_name,name+".jpg"))

def test_new_visitor(user_name,session):
    permitted_visitors=session.query(Visitor).filter_by(user_name=user_name)
    new_visitor_photo=open(img_full_path("imgs","musk2.jpg"),'rb').read()
    for v in permitted_visitors:
        if is_match(new_visitor_photo,v.photo):
            return True
    return False

def main():
    """ temp_visitor=session.query(Visitor).first()
    photo=temp_visitor.photo
    print(type(photo))
    print(temp_visitor.visitor_id,temp_visitor.name,temp_visitor.user_id) """
    # init_DB()
    DB_ops.show_all_data(session)
    print(test_new_visitor("bob",session))

if __name__=="__main__":
    main()