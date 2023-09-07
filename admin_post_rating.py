import os

from flask import request, redirect, flash, Blueprint

from config import config
from db_model import db, Post, Location
from helpers import render, admin_required

rating_blueprint = Blueprint('rating', __name__, template_folder='templates', static_folder='static')


@rating_blueprint.route('/admin/new_posts')
@admin_required
def new_posts_list():
    posts = Post.query.filter(Post.approved.is_(None)).order_by(Post.timestamp).all()
    locations = Location.query.all()
    return render("new_posts_list.html", posts=posts, locations=locations)


@rating_blueprint.route('/admin/new_posts/<id_location>')
@admin_required
def new_posts_list_at_location(id_location):
    posts = Post.query.filter(Post.approved.is_(None)).filter_by(id_location=id_location).order_by(Post.timestamp).all()
    locations = Location.query.all()
    current_location = Location.query.get(id_location)
    return render("new_posts_list.html", posts=posts, locations=locations, current_location=current_location)


@rating_blueprint.route('/admin/rate/<id_post>')
@admin_required
def post_rating(id_post):
    post: Post = Post.query.get(id_post)
    if post is None:
        flash(f"Příspěvěk s id_post={id_post} neexistuje.", "warning")
        return redirect("/admin/new_posts")

    return render("post_rating.html", post=post)


def rate_post(id_post, approved):
    post: Post = Post.query.get(id_post)
    if post is None:
        flash(f"Příspěvěk s id_post={id_post} neexistuje.", "warning")
        return redirect("/admin/new_posts")

    old_file_path = post.file_path

    post.approved = approved
    db.session.add(post)
    db.session.commit()

    new_file_path = post.file_path
    os.rename(old_file_path, new_file_path)

    flash("Příspěvek potrvrzen." if approved else "Příspěvek zamítnut.", "success")

    return redirect(f"/admin/new_posts/{post.id_location}")


@rating_blueprint.route('/admin/rate/<id_post>/approve', methods=['POST'])
@admin_required
def post_approve(id_post):
    return rate_post(id_post, True)


@rating_blueprint.route('/admin/rate/<id_post>/reject', methods=['POST'])
@admin_required
def post_reject(id_post):
    return rate_post(id_post, False)
