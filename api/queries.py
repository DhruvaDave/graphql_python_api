from traceback import print_tb
from ariadne import ObjectType, convert_kwargs_to_snake_case
from sqlalchemy import or_, func, and_
from models.tbl_post import TblPost
from models.tbl_user import TblUser

def listPosts_resolver(obj, info):
    try:
        posts = [post.to_json() for post in TblPost.query.all()]
        payload = {
            "success": True,
            "posts": posts
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

def searchPosts_resolver(obj, info, searchString):
    try:
        posts = [post.to_json() for post in TblPost.query.filter(
                or_(
                    TblPost.title.contains(searchString),
                    TblPost.description.contains(searchString)
                )
            )
        .all()]
        payload = {
            "success": True,
            "posts": posts
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

def getPost_resolver(obj, info, post_id):
    try:
        posts = TblPost.query.join(
                TblUser, TblUser.user_id == TblPost.user_id_fk
            ).filter(
                TblPost.post_id == post_id).all()

        res = []
        post = {
            "post_id": post_id,
            "title": posts[0].title
        }
        for post in posts:
            user = TblUser.query.get(post.user_id_fk)
            res.append({
                "user_id":post.user_id_fk,
                "first_name": user.first_name 
            })
        payload = {
            "success": True,
            "post": post,
            "users": res
        }
    except AttributeError:  
        payload = {
            "success": False,
            "errors": ["Post item matching {id} not found"]
        }
    return payload

