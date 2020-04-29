from flask import Flask,render_template,url_for,flash,redirect,request
from flaskapp.forms import RegistrationForm,LoginForm,UpdateAccountForm,AddVisitorForm,VisitorIdentificationForm,UpdateVisitorForm
from flaskapp import app,bcrypt,db
from flaskapp.models import User,Visitor,VisitRecord
from flask_login import login_user,current_user,logout_user,login_required
import secrets
import os
from PIL import Image
from flaskapp.AWS_API import is_match

@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash("You have already logged in",'info')
        return redirect(url_for('account'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            flash("Successfully logged in",'success')
            # ternery operator in python
            # directly redirect to target page that the user want to visit before logged in
            return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash("Login unsuccessful, please check username and password",'danger')
    return render_template('login.html',title='Login',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_pw=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user=User(username=form.username.data,email=form.email.data,password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Account with email: {form.email.data} is created.",'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("Successfully logged out.",'success')
    return redirect(url_for('login'))

@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash("Account info is updated!",'success')
        # post-get-redirect pattern
        return redirect(url_for('account'))
    else:
        form.username.data=current_user.username
        form.email.data=current_user.email
        return render_template('account.html',title='Account',form=form)

@app.route('/visitors')
@login_required
def visitors():
    # show all visitors in user account page
    all_visitors=Visitor.query.filter_by(user_id=current_user.id)
    return render_template('visitors.html',title="Visitors",visitors=all_visitors)

def save_visitor_photo(form_picture,folder_name):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    hashed_photo_name=random_hex+f_ext
    photo_path=os.path.join(app.root_path,'static/%s' % folder_name,hashed_photo_name)
    res_image=Image.open(form_picture)
    res_image.save(photo_path)
    return hashed_photo_name,photo_path

@app.route('/add_visitor',methods=['GET','POST'])
@login_required
def add_visitor():
    form=AddVisitorForm()
    if form.validate_on_submit():
        photo_name,_=save_visitor_photo(form.photo.data,'visitor_photos')
        new_visitor=Visitor(name=form.name.data,photo=photo_name,user_id=current_user.id)
        db.session.add(new_visitor)
        db.session.commit()
        flash(f"New visitor added: {form.name.data}",'success')
        return redirect(url_for('visitors'))

    return render_template('add_visitor.html',title="Add Visitor",form=form)

def identify_visitor(photo_path):
    visitors=Visitor.query.filter_by(user_id=current_user.id)
    for visitor in visitors:
        visitor_photo_path=os.path.join(app.root_path,'static','visitor_photos',visitor.photo)
        photo_file=open(visitor_photo_path,'rb').read()
        if is_match(open(photo_path,'rb').read(),photo_file):
            return True,visitor.id
    return False,None

@app.route('/identify',methods=['GET','POST'])
@login_required
def identify():
    form=VisitorIdentificationForm()
    if request.method=='POST':
        photo_name,photo_path=save_visitor_photo(form.photo.data,'identify_visitors')
        identify_res,visitor_id=identify_visitor(photo_path)
        if identify_res:
            # this is a permitted visitor
            visitor=Visitor.query.get(visitor_id)
            record=VisitRecord(photo=photo_name,user_id=current_user.id,visitor_id=visitor_id,visitor=visitor)
            db.session.add(record)
            db.session.commit()
            return redirect(url_for('permitted'))
        else:
            # this is a denined visitor
            record=VisitRecord(photo=photo_name,user_id=current_user.id)
            db.session.add(record)
            db.session.commit()
            return redirect(url_for('denied'))
    return render_template('identify.html',title="Identify",form=form)

@app.route('/permitted')
@login_required
def permitted():
    return render_template('permitted.html')

@app.route('/denied')
@login_required
def denied():
    return render_template('denied.html')

@app.route('/records')
@login_required
def records():
    visit_records=VisitRecord.query.filter_by(user_id=current_user.id)
    return render_template('records.html',title="Records",visit_records=visit_records)

@app.route('/update_visitor/<int:visitor_id>',methods=['GET','POST'])
def update_visitor(visitor_id):
    form=UpdateVisitorForm()
    visitor=Visitor.query.get(visitor_id)
    records=VisitRecord.query.filter_by(visitor_id=visitor_id)
    if request.method=='GET':
        form.name.data=visitor.name
        return render_template('update_visitor.html',visitor=visitor,visit_records=records,form=form)
    elif form.validate_on_submit():
        visitor.name=form.name.data
        if form.photo.data:
            photo_name,_=save_visitor_photo(form.photo.data,'visitor_photos')
            visitor.photo=photo_name
        db.session.commit()
        flash("Visitor info is updated.",'success')
        return redirect(url_for('update_visitor',visitor_id=visitor_id))
