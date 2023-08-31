from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

from abstract import Abstract

db = SQLAlchemy()
bcrypt = Bcrypt()


class AbstractUser(UserMixin, Abstract):

    __required_attributes__ = ["name"]

    @property
    def is_admin(self):
        return False

    @property
    def id(self):
        return


class Admin(AbstractUser):

    @property
    def is_admin(self):
        return True

    @property
    def id(self):
        return -1

    name = "admin"


class User(db.Model, AbstractUser):

    __tablename__ = "users"

    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    note = db.Column(db.Text, nullable=True)

    @property
    def id(self):
        return self.id_user

    def __init__(self, name, password_plain, note):
        self.name = name
        self.set_password(password_plain)
        self.note = note

    def set_password(self, password_plain):
        self.password = bcrypt.generate_password_hash(password_plain)
