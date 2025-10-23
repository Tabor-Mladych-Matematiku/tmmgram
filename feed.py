from flask import Blueprint
from flask_login import login_required

from db_model import Post
from helpers import render
from datetime import datetime

feed_blueprint = Blueprint('feed', __name__, template_folder='templates', static_folder='static')


@feed_blueprint.route('/')
@login_required
def render_feed():
    posts: list[Post] = (Post.query
                         .filter(Post.approved.is_(True))
                         .order_by(Post.timestamp.desc())
                         .limit(10)
                         .all())
    # Format the timestamp in Czech format (DD.MM.YYYY HH:MM)
    for post in posts:
        post.time = post.timestamp.strftime('%d.%m.%Y %H:%M')
    return render('index.html', posts=posts)
