from flask import Blueprint
from flask_login import login_required

from db_model import Post
from helpers import render

feed_blueprint = Blueprint('feed', __name__, template_folder='templates', static_folder='static')


@feed_blueprint.route('/')
@login_required
def render_feed():
    posts: list[Post] = Post.query.order_by(Post.timestamp.desc()).limit(10).all()
    return render('index.html', posts=posts)
