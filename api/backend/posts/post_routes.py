from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db


@post.route("/p/posts", methods = ["POST"])
def create_post():
    data = request.json
    query = """
    INSERT INTO post (is_public, created_at, c)
    """
    return 