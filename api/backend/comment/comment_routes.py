from flask import Blueprint, jsonify, request
from backend.db_connection import db

comments = Blueprint('comments', __name__)

@comments.route('', methods=['GET'])
def get_comments():
    query = '''
        SELECT id, NUID, date, text
        FROM comment
        ORDER BY date DESC
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return jsonify(data)