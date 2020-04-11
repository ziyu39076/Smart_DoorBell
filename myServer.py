from sqlalchemy import Column, ForeignKey, Integer, String,LargeBinary
# import this declarative base to inherate
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker
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

# link to the DB we are using
# pay attention to this part, if without check_same_thread=false, there will be lots of errors
# but what is going on behind this part of code
# what does engine and session really means
engine = create_engine('sqlite:///data.db',connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

from flask import Flask, render_template, request, redirect, url_for, jsonify
from AWS_API import is_match
from datetime import datetime
from flask_mail import Mail, Message
# create an instance of my app 
app = Flask(__name__)

system_email='zyz39298@gmail.com'
# configuration of mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = system_email
app.config['MAIL_PASSWORD'] = "gmailcode"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
@app.route('/users/')
def users():
	# list all users as links
	users=session.query(User).all()
	return render_template('users.html',users=users)

@app.route('/users/add',methods=['GET','POST'])
def add_user():
	if request.method=='GET':
		return render_template('add_user.html')
	else:
		new_name=request.form['name']
		new_email=request.form['email']
		try:
			session.query(User).filter_by(name=new_name).one()
			# if no exception raised, means the user is already in the system
			return redirect(url_for('fail_add_user'))
		except:
			new_user=User(name=new_name,email=new_email)
			session.add(new_user)
			session.commit()
			return redirect(url_for('users'))

# how to integrate this function to add_user method
@app.route('/users/add/fail',methods=['GET','POST'])
def fail_add_user():
	if request.method=='GET':
		return render_template('fail_add_user.html')
	else:
		new_name=request.form['name']
		new_email=request.form['email']
		try:
			user=session.query(User).filter_by(name=new_name).one()
			# if no exception raised, means the user is already in the system
			return redirect(url_for('fail_add_user'))
		except:
			new_user=User(name=new_name,email=new_email)
			session.add(new_user)
			session.commit()
			return redirect(url_for('users'))

@app.route('/users/<string:user_name>/')
def user_dashboard(user_name):
	# attention, query opj.one() is what we needed
	user=session.query(User).filter_by(name=user_name).one()
	return render_template('user_dashboard.html',user=user)

@app.route('/users/<string:user_name>/edit-email',methods=['GET','POST'])
def edit_email(user_name):
	if request.method=='GET':
		return render_template('edit_email.html',user_name=user_name)
	else:
		target_user=session.query(User).filter_by(name=user_name).one()
		target_user.email=request.form['email']
		session.add(target_user)
		session.commit()
		return redirect(url_for('user_dashboard',user_name=user_name))

@app.route('/users/<string:user_name>/identify/',methods=['GET','POST'])
def identify(user_name):
	user=session.query(User).filter_by(name=user_name).one()
	# identify new visitor and post visit record
	if request.method=='GET':
		return render_template('identify.html',user_name=user_name)
	else:
		time=datetime.now().strftime("%c")
		visitor_photo=request.files['img'].read()
		permitted_visitors=session.query(Visitor).filter_by(user_name=user_name)
		for v in permitted_visitors:
			print(v.name)
			if is_match(visitor_photo,v.photo):
				# create new visit record
				new_visit_record=VisitRecord(date=time,
											 user_name=user_name,
											 visitor_id=v.visitor_id,
											 visitor_name=v.name)
				session.add(new_visit_record)
				session.commit()				
				return redirect(url_for('permitted',visitor_name=v.name,user_name=user_name))
				# add a visit record and redirect to user_dashboard
		# did not find any match
		# create stranger visit record
		new_visit_record=VisitRecord(date=time,
									 user_name=user_name,
									 visitor_name="stranger")
		session.add(new_visit_record)
		session.commit()
		# send alert message to user
		alert_message=Message("Alert from Smart Door Bell",sender=system_email,recipients=[user.email])
		alert_message.body="A stranger visited your home at %s" % time
		mail.send(alert_message)
		return redirect(url_for('denied',user_name=user_name))
		# add a stranger visit and redirect to user_dashboard

# strange rule: para list in decorator must match para list in function
@app.route('/users/<string:user_name>/identify/<string:visitor_name>/permitted')
def permitted(visitor_name,user_name):
	return render_template('permitted_visitor.html',visitor_name=visitor_name,user_name=user_name)

@app.route('/users/<string:user_name>/identify/denied')
def denied(user_name):
	return render_template('denied_visitor.html',user_name=user_name)

@app.route('/users/<string:user_name>/history/')
def visit_history(user_name):
	# list all visit records
	visit_records=session.query(VisitRecord).filter_by(user_name=user_name)
	return render_template('visit_history.html',user_name=user_name,visit_records=visit_records)
	
@app.route('/users/<string:user_name>/visitors/')
def user_visitors(user_name):
	# list all permitted visitors for a user
	visitors=session.query(Visitor).filter_by(user_name=user_name)
	return render_template('visitors.html',user_name=user_name,visitors=visitors)

@app.route('/users/<string:user_name>/visitors/new/',methods=['GET','POST'])
# adding new visitor is finished by user manually
def add_new_visitor(user_name):
	if request.method=='GET':
		return render_template('add_new_visitor.html',user_name=user_name)
	else:
		new_visitor=Visitor(name=request.form['name'],photo=request.files['img'].read(),user_name=user_name)
		session.add(new_visitor)
		session.commit()
		return redirect(url_for('user_visitors',user_name=user_name))

@app.route('/users/<string:user_name>/visitors/<int:visitor_id>/edit/',methods=['GET','POST'])
def user_edit_visitor(user_name, visitor_id):
	target_visitor=session.query(Visitor).filter_by(visitor_id).one()
	if request.method=='GET':
		return render_template('edit_visitor',user_name=user_name,target_visitor=target_visitor)
	else:
		# update name and photo
		target_visitor.name=request.form['name']
		target_visitor.photo=request.files['img'].read()
		session.add(target_visitor)
		session.commit()
		return render_template(url_for('user_visitors'),user_name=user_name)

@app.route('/users/<string:user_name>/visitors/<int:visitor_id>/delete/',methods=['GET','POST'])
def user_delete_visitor(user_name, visitor_id):
	target_visitor=session.query(Visitor).filter_by(visitor_id=visitor_id).one()
	if request.method=='POST':
		session.delete(target_visitor)
		session.commit()
		return redirect(url_for('user_dashboard',user_name=user_name))
	else:
		return render_template('delete_visitor.html',user_name=user_name,visitor_id=visitor_id,target_visitor=target_visitor)

if __name__ == "__main__": 
    app.run()
	