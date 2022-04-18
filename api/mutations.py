# mutations.py
from datetime import date
from utils.db_handler import handler
from models.tbl_post import TblPost


db_session = handler.db_session

def create_post_resolver(obj, info, title, description):
    try:
        today = date.today()
        post = TblPost(
            title=title, description=description, created_at=today
        )
        db_session.add(post)
        db_session.commit()
        payload = {
            "success": True,
            "post": post.to_json()
        }
    except Exception as ex:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Exception occured {ex} "]
        }
    return payload

def update_post_resolver(obj, info, post_id, title=False, description=False):
    try:
        post = TblPost.query.get(post_id)
        if post:
            if title:
                post.title = title
            if description:
                post.description = description
        db_session.add(post)
        db_session.commit()
        payload = {
            "success": True,
            "post": post.to_json()
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": ["item matching id {id} not found"]
        }
    return payload

def delete_post_resolver(obj, info, post_id):
    try:
        post = TblPost.query.get(post_id)
        db_session.delete(post)
        db_session.commit()
        payload = {"success": True, "post": post.to_json()}
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Not found"]
        }
    return payload
