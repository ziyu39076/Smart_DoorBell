from datetime import datetime
from flaskapp import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):

    __tablename__="user"

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=False,unique=True)
    email=db.Column(db.String(100),nullable=False,unique=True)
    password=db.Column(db.String(60),nullable=False)
    # build relationship with other forms
    visitors=db.relationship('Visitor',backref='user',lazy=True)
    records=db.relationship('VisitRecord',backref='user',lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

class Visitor(db.Model):

    __tablename__="visitor"

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    photo=db.Column(db.String(20),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    records=db.relationship('VisitRecord',backref='visitor',lazy=True)

    def __repr__(self):
        return f"Visitor('{self.name}','{self.photo}')"
    
class VisitRecord(db.Model):

    __tablename__="visit_record"

    id=db.Column(db.Integer,primary_key=True)
    # datatime.ucnow pass in a function as an argument
    photo=db.Column(db.String(20),nullable=False)
    date_visited=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    visitor_id=db.Column(db.Integer,db.ForeignKey('visitor.id'))

    def __repr__(self):
        return f"Record(visitor:'{self.visitor_id}',date:'{self.date_visited}')"