from typing import Any, cast

from flask import redirect, flash, Blueprint, request
from flask_login import current_user, login_required

from db_model import User, Post
from helpers import render

profile_blueprint = Blueprint('profile', __name__, template_folder='templates', static_folder='static')
PROFILE_POST_FEED_LIMIT = 10


def _get_feed_filter(feed):
    if feed == "pending":
        return None
    if feed == "rejected":
        return False
    return True


def _query_profile_posts(user: User, feed: str, limit: int, offset: int):
    approved = _get_feed_filter(feed)
    return (Post.query
            .filter_by(id_user=user.id_user)
            .filter(Post.approved.is_(approved))
            .order_by(cast(Any, Post.timestamp).desc())
            .offset(offset)
            .limit(limit)
            .all())


@profile_blueprint.route('/profile')
@login_required
def profile_current():
    return render_profile(cast(User, current_user))


@profile_blueprint.route('/profile/<name>')
@login_required
def profile(name):
    user: User = User.query.filter_by(name=name).first()
    if user is None:
        flash(f"Uživatel {name} neexistuje.", "warning")
        return redirect("/")
    return render_profile(user)


@profile_blueprint.route('/profile/<name>/<feed>')
@login_required
def profile_feed(name, feed):
    user: User = User.query.filter_by(name=name).first()
    if user is None:
        flash(f"Uživatel {name} neexistuje.", "warning")
        return redirect("/")
    if feed not in ("pending", "rejected"):
        flash(f"Neplatný stav příspěvku: {feed}.", "warning")
        return redirect(f"/profile/{name}")
    return render_profile(user, feed)


def render_profile(user: User, feed="approved"):
    posts = _query_profile_posts(user, feed, PROFILE_POST_FEED_LIMIT, 0)
    return render('profile.html', user=user, posts=posts, feed=feed, post_feed_limit=PROFILE_POST_FEED_LIMIT)


@profile_blueprint.route('/profile/<name>/posts')
@profile_blueprint.route('/profile/<name>/<feed>/posts')
@login_required
def profile_posts(name, feed="approved"):
    user: User = User.query.filter_by(name=name).first()
    if user is None:
        return ""

    limit = request.args.get('limit', PROFILE_POST_FEED_LIMIT, type=int)
    offset = request.args.get('offset', 0, type=int)

    if limit is None or limit < 1:
        limit = PROFILE_POST_FEED_LIMIT
    if offset is None or offset < 0:
        offset = 0

    posts = _query_profile_posts(user, feed, limit, offset)
    return render('posts.html', posts=posts)
