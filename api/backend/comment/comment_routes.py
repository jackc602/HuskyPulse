from flask import Blueprint, jsonify, request, make_response
from backend.db_connection import db

comments = Blueprint('comments', __name__)

@comments.route('', methods=['GET'])
def get_comments():
    nuid = request.args.get('nuid')

    query = '''
        SELECT id, NUID, date, text
        FROM comment
        WHERE (%s IS NULL OR NUID = %s)
        ORDER BY date DESC
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (nuid, nuid))
    data = cursor.fetchall()
    return jsonify(data)

# Get comments made on a given post
@comments.route("/post", methods = ["GET"])
def get_post_comments():
    post_id = request.args.get("post_id")
    query = """
    SELECT s.first_name AS first, s.last_name AS last, c.text AS content, c.date AS date_posted
    FROM student s JOIN comment c JOIN post_comment pc
    ON s.NUID = c.NUID AND c.id = pc.comment_id
    WHERE pc.post_id = %s
    """
    params = (post_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# Create a comment on a given post
@comments.route("/post", methods = ["POST"])
def make_comment():
    data = request.json
    query1 = """
    INSERT INTO comment (NUID, text)
    VALUES (%s, %s)
    """
    params1 = (data["nuid"], data["comment"])
    query2 = """
    INSERT INTO post_comment (post_id, comment_id)
    VALUES (%s, %s)
    """
    cursor = db.get_db().cursor()
    cursor.execute(query1, params1)
    params2 = (data["post_id"], cursor.lastrowid)
    cursor.execute(query2, params2)
    db.get_db().commit()
    response = make_response("Successfully created comment")
    response.status_code = 200
    return response
