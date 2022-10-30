from flask import Flask
from config import Config
from flask_migrate import Migrate
from .models import db, User
from flask_login import LoginManager

app = Flask(__name__)

login = LoginManager(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login.init_app(app)
login.login_view = 'login'

from app import routes, models