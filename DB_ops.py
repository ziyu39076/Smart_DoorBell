from DB_setup_alchemy import User,Visitor

# user DB operations
def create_new_user(user_name,user_email,session):
    try:
        new_user=User(name=user_name,email=user_email)
        session.add(new_user)
        session.commit()
    except:
        print("a user with name: %s aready exists in the database" % user_name)

""" def update_user_info(input_id,new_name,new_email,session):
    try:
        target_user=session.query(User).filter_by(user_id=input_id).one()
        target_user.name=new_name
        target_user.email=new_email
        session.add(target_user)
        session.commit()
    except:
        print("user with id=%d is not found" % input_id) """

def delete_user(user_name,session):
    try:
        target_res=session.query(User).filter_by(name=user_name).one()
        if target_res!=[]:
            session.delete(target_res)
            session.commit()
    except:
        print("user with name=%s is not found" % user_name)

# visitor DB operations
def add_new_visitor(input_user_name,visitor_name,visitor_photo,session):
    new_visitor=Visitor(name=visitor_name,photo=visitor_photo,user_name=input_user_name)
    session.add(new_visitor)
    session.commit()

def update_visitor_photo(input_visitor_id,new_photo,session):
    try:
        target_visitor=session.query(Visitor).filter_by(visitor_id=input_visitor_id).one()
        target_visitor.photo=new_photo
        session.add(target_visitor)
        session.commit()
    except:
        print("visitor with id=%d is not found" % input_visitor_id)

def delete_visitor(input_visitor_id,session):
    try:
        target_visitor=session.query(Visitor).filter_by(visitor_id=input_visitor_id).one()
        session.delete(target_visitor)
        session.commit()
    except:
        print("visitor with id=%d is not found" % input_visitor_id)

# show all data in db
def show_all_data(session):
    users=session.query(User).all()
    for user in users:
        print("user:",user.name)
        print("email:",user.email)
        visitors=session.query(Visitor).filter_by(user_name=user.name)
        for visitor in visitors:
            print("visitor:",visitor.visitor_id,visitor.name)