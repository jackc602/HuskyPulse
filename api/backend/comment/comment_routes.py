from flask import Blueprint, jsonify, request
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