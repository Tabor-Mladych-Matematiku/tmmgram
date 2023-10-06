from flask import redirect, flash, Blueprint
from flask_login import current_user, login_required

from db_model import User, Post
from helpers import render

profile_blueprint = Blueprint('profile', __name__, template_folder='templates', static_folder='static')


@profile_blueprint.route('/profile')
@login_required
def profile_current():
    return render_profile(current_user)


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
    if feed == "pending":
        approved = None
    elif feed == "rejected":
        approved = False
    else:
        approved = True

    posts: list[Post] = (Post.query
                         .filter_by(id_user=user.id_user)
                         .filter(Post.approved.is_(approved))
                         .order_by(Post.timestamp.desc())
                         .all())
    return render('profile.html', user=user, posts=posts, feed=feed)
