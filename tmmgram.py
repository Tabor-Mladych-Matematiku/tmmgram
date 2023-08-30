from flask import Flask
from flask_login import LoginManager, login_required

from db_model import db, bcrypt, Admin, User
from config import config
from helpers import render

app = Flask(__name__)
app.secret_key = config['secret']
app.config["DEBUG"] = True

# Timezone configuration

try:  # Linux only
    import os
    from time import tzset
    os.environ['TZ'] = config['timezone']
    tzset()
except ImportError:
    pass

# Database configuration

if 'db' in config:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
        username=config['db']['user'],
        password=config['db']['password'],
        hostname=config['db']['hostname'],
        databasename=config['db']['database'],
    )
else:
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.sqlite"

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
bcrypt.init_app(app)

# Login configuration

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login.login"
login_manager.login_message_category = "info"
login_manager.login_message = "Pro zobrazení stránky se přihlaste."


@login_manager.user_loader
def load_user(user_id):
    if user_id == "-1":
        return Admin()
    else:
        return User.query.get(int(user_id))


from login import login_blueprint
app.register_blueprint(login_blueprint)


@app.route('/')
@login_required
def index():
    return render("index.html")

