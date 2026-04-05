from typing import Any, cast

from flask import Blueprint, request
from flask_login import login_required

from db_model import Post
from helpers import render
from likes_helpers import get_likes_data

POST_FEED_LIMIT = 10

feed_blueprint = Blueprint('feed', __name__, template_folder='templates', static_folder='static')


@feed_blueprint.route('/')
@login_required
def render_feed():
    posts: list[Post] = (Post.query
                         .filter(Post.approved.is_(True))
                         .order_by(cast(Any, Post.timestamp).desc())
                         .limit(POST_FEED_LIMIT)
                         .all())
    likes_count_by_post_id, liked_post_ids = get_likes_data(posts)
    return render('index.html',
                  posts=posts,
                  post_feed_limit=POST_FEED_LIMIT,
                  likes_count_by_post_id=likes_count_by_post_id,
                  liked_post_ids=liked_post_ids)

@feed_blueprint.route('/posts')
@login_required
def render_posts():
    limit = request.args.get('limit', POST_FEED_LIMIT, type=int)
    offset = request.args.get('offset', 0, type=int)

    if limit is None or limit < 1 or limit > POST_FEED_LIMIT:
        limit = POST_FEED_LIMIT
    if offset is None or offset < 0:
        offset = 0

    posts: list[Post] = (Post.query
                         .filter(Post.approved.is_(True))
                         .order_by(cast(Any, Post.timestamp).desc())
                         .offset(offset)
                         .limit(limit)
                         .all())
    likes_count_by_post_id, liked_post_ids = get_likes_data(posts)
    return render('posts.html',
                  posts=posts,
                  likes_count_by_post_id=likes_count_by_post_id,
                  liked_post_ids=liked_post_ids)
