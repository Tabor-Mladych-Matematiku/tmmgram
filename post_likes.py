from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from db_model import db, Post, PostLike, User

post_likes_blueprint = Blueprint('post_likes', __name__, template_folder='templates', static_folder='static')


@post_likes_blueprint.route('/posts/<int:id_post>/like-toggle', methods=['POST'])
@login_required
def like_toggle(id_post):
    if current_user.is_admin:
        return jsonify({'error': 'Admins cannot like posts.'}), 403

    post: Post = Post.query.get(id_post)
    if post is None:
        return jsonify({'error': 'Post does not exist.'}), 404
    if not post.approved:
        return jsonify({'error': 'Only approved posts can be liked.'}), 400

    user: User = current_user
    like: PostLike = (PostLike.query
                      .filter(PostLike.id_post == post.id_post)
                      .filter(PostLike.id_user == user.id_user)
                      .first())

    if like is None:
        db.session.add(PostLike(id_post=post.id_post, id_user=user.id_user))
        liked = True
    else:
        db.session.delete(like)
        liked = False

    db.session.commit()

    return jsonify({
        'liked': liked,
        'likes_count': post.likes_count,
    })