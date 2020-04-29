from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app=Flask(__name__)

# use secrets module in python to generate random string
# secrets.token_hex(16), 16 is length of token
app.config['SECRET_KEY']='eb79b747065c9573537396f23d6ee961'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'

# link db with app
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

from flaskapp import routes