from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from backend.db_connection import db

posts = Blueprint("posts", __name__)

# retrieve all posts that should be visible to a given student
@posts.route("/posts/student", methods = ["GET"])
def fetch_posts():
    student_NUID = request.args.get("nuid")
    query = """
    SELECT p.*
    FROM post p JOIN club c JOIN student_club sc JOIN student s
    ON p.club_id = c.id AND c.id = sc.club_id AND sc.NUID = s.NUID
    WHERE p.is_public = 1 OR s.NUID = %s
    """
    params = (student_NUID)
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# Fetch all posts made by a certain club
@posts.route("/posts/club", methods = ["GET"])
def fetch_club_posts():
    club_id = request.args.get("club_id")
    query = """
    SELECT *
    FROM post p
    WHERE p.club_id = %s
    """
    params = (club_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# create a new post in the database
@posts.route("/posts", methods = ["POST"])
def create_post():
    data = request.json
    query = """
    INSERT INTO post (is_public, club_id, title, description, image_file)
    VALUES (%s, %s, %s, %s, %s)
    """
    params = (data["is_public"], data["club_id"], data["title"], 
              data["description"], data["image_file"])
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    response = make_response("Successfully created new post")
    response.status_code = 200
    return response

# get a single post based on post id
@posts.route("/posts", methods = ["GET"])
def fetch_single_post():
    post_id = request.args.get("post_id")
    query = """
    SELECT *
    FROM post p
    WHERE p.id = %s
    """
    params = (post_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# update a post that has already been made 
@posts.route("/update", methods = ["POST"])
def update_post():
    post_data = request.json
    query = """
    UPDATE post
    SET title = %s, description = %s, club_id = %s, event_id = %s, 
    is_public = %s, image_file = %s
    WHERE post.id = %s
    """
    params = (post_data["title"], post_data["description"], post_data["club_id"], 
              post_data["event_id"], post_data["is_public"], post_data["image_file"],
              post_data["post_id"])
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    response = make_response("Successfully updated post")
    response.status_code = 200
    return response
