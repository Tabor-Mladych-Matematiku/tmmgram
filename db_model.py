import os
from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import relationship, backref

from abstract import Abstract
from config import config

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

    @property
    def is_verified(self):
        return self.name.lower() == "elis"

    @property
    def name_with_badge(self):  # use with "| safe" flask filter to render HTML
        return self.name + (' <i class="bi bi-patch-check-fill text-info"></i>' if self.is_verified else '')

    @property
    def followers(self):
        post_followers = (db.session.query(func.sum(Post.followers))
                          .filter(Post.id_user == self.id_user)
                          .filter(Post.approved.is_(True))
                          .first())[0]
        if post_followers is None:
            post_followers = 0
        # TODO: add "fake followers"
        return post_followers


class Location(db.Model):
    __tablename__ = "locations"

    id_location = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    followers_coefficient = db.Column(db.Float, nullable=False)

    def __init__(self, name, followers_coefficient):
        self.name = name
        self.followers_coefficient = followers_coefficient


class Post(db.Model):

    __tablename__ = "posts"

    id_post = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey(User.id_user, ondelete='RESTRICT'))
    filename = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime)
    id_location = db.Column(db.Integer, db.ForeignKey(Location.id_location, ondelete='RESTRICT'))
    description = db.Column(db.Text, nullable=False, default='')

    approved = db.Column(db.Boolean, nullable=True, default=None)
    followers = db.Column(db.Integer, nullable=True, default=None)

    # save the rating values for reference
    task_points = db.Column(db.Integer, nullable=True, default=None)
    photo_points = db.Column(db.Integer, nullable=True, default=None)
    followers_at_time_of_post = db.Column(db.Integer, nullable=True, default=None)

    # relationships
    user = relationship("User", backref=backref("users", uselist=False))
    location = relationship("Location", backref=backref("locations", uselist=False))

    def __init__(self, filename, id_user, id_location, description):
        self.id_user = id_user
        self.id_location = id_location
        self.filename = filename
        self.description = description
        self.timestamp = datetime.now()

    @property
    def src(self):
        return "/photos/" + self.filename

    @property
    def file_path(self):
        if self.approved is None:
            return os.path.join(config['upload_folder'], self.filename)
        elif self.approved:
            return os.path.join(config['approved_folder'], self.filename)
        else:
            return os.path.join(config['rejected_folder'], self.filename)

    @property
    def time(self):
        return self.timestamp.strftime("%H:%M")
