from flask import Flask, render_template, request, redirect, url_for, jsonify
# create an instance of my app 
app = Flask(__name__)

# import all dependencies to create link to database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB_setup_alchemy import Base, User, Visitor,VisitRecord

# pay attention to this part, if without check_same_thread=false, there will be lots of errors
# but what is going on behind this part of code
# what does engine and session really means
engine = create_engine('sqlite:///data.db',connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

""" @app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in items]) """

@app.route('/')
@app.route('/users/')
def users():
	# list all users as links
	users=session.query(User).all()
	return render_template('users.html',users=users)

@app.route('/users/<string:user_name>/')
def user_info(user_name):
	return render_template('user_info.html',user_name=user_name)

@app.route('/users/<string:user_name>/history/')
def visit_history(user_name):
	
	""" visit_records=session.query(VisitRecord).filter_by(user_name=user_name)
	return render_template('visit_history.html',user_name=user_name,visit_records=visit_records) """

	return "history database is not created"

@app.route('/users/<string:user_name>/history/new')
def add_visit_history(user_name):
	# add post method to this function
	return "add_visit_history"

@app.route('/users/<string:user_name>/visitors/')
def user_visitors(user_name):
	visitors=session.query(Visitor).filter_by(user_name=user_name)
	return render_template('visitors.html',user_name=user_name,visitors=visitors)
	""" for v in visitors:
		print(v.name) """
	""" return "all visitors" """

@app.route('/users/<string:user_name>/visitors/new/')
def add_new_visitor(user_name):
	return "add_new_visitor"

@app.route('/users/<string:user_name>/visitors/<int:visitor_id>/edit/')
def user_edit_visitor(user_name, visitor_id):
	return "user_edit_visitor"

@app.route('/users/<string:user_name>/visitors/<int:visitor_id>/delete/',methods=['GET','POST'])
def user_delete_visitor(user_name, visitor_id):
	target_visitor=session.query(Visitor).filter_by(visitor_id=visitor_id).one()
	if request.method=='POST':
		session.delete(target_visitor)
		session.commit()
		return redirect(url_for('user_info',user_name=user_name))
	else:
		return render_template('delete_visitor.html',user_name=user_name,visitor_id=visitor_id,target_visitor=target_visitor)

if __name__ == '__main__':
	app.debug = True
	app.run(host = '127.0.0.1', port = 5000)