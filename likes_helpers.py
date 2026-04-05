from flask_login import current_user
from sqlalchemy import func

from db_model import Post, PostLike


def get_likes_data(posts: list[Post]):
    post_ids = [post.id_post for post in posts]
    if len(post_ids) == 0:
        return {}, set()

    likes_count_rows = (PostLike.query
                        .with_entities(PostLike.id_post, func.count(PostLike.id_post_like))
                        .filter(PostLike.id_post.in_(post_ids))
                        .group_by(PostLike.id_post)
                        .all())
    likes_count_by_post_id = {id_post: count for id_post, count in likes_count_rows}

    liked_post_ids = set()
    if not current_user.is_admin:
        liked_rows = (PostLike.query
                      .with_entities(PostLike.id_post)
                      .filter(PostLike.id_post.in_(post_ids))
                      .filter(PostLike.id_user == current_user.id_user)
                      .all())
        liked_post_ids = {id_post for id_post, in liked_rows}

    return likes_count_by_post_id, liked_post_ids
