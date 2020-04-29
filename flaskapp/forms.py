from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flaskapp.models import User,VisitRecord,Visitor

# create form class to represent forms in html
class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=2,max=20)])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign up')

    # define inline-validator like this validate_fieldname
    def validate_username(self,username):
        try: 
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("This username is taken, please try a different one.")
        except:
            pass
    
    def validate_email(self,email):
        try: 
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("This email is taken, please try a different one.")
        except:
            pass

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Log in')

class UpdateAccountForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('Update')

    # define inline-validator like this validate_fieldname
    def validate_username(self,username):
        # if user does not change any data field, then do not need to check
        if username.data!=current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("This username is taken, please try a different one.")
    
    def validate_email(self,email):
        if email.data!=current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("This email is taken, please try a different one.")

class AddVisitorForm(FlaskForm):
    name=StringField('name',validators=[DataRequired(),Length(min=2,max=20)])
    photo=FileField("Upload visitor photo",validators=[DataRequired(),FileAllowed(['jpg','png','bmp','tif'])])
    submit=SubmitField('Add visitor')

class UpdateVisitorForm(FlaskForm):
    name=StringField('name',validators=[DataRequired(),Length(min=2,max=20)])
    photo=FileField("Upload visitor photo",validators=[FileAllowed(['jpg','png','bmp','tif'])])
    submit=SubmitField('Update')

class VisitorIdentificationForm(FlaskForm):
    photo=FileField("Upload visitor photo",validators=[DataRequired(),FileAllowed(['jpg','png','bmp','tif'])])
    submit=SubmitField('Identify')