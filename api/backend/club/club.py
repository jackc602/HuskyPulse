from flask import Blueprint, request, jsonify, make_response
from datetime import datetime
from backend.db_connection import db

# making the blueprint for club
club = Blueprint('clubs', __name__)  

# ---------------- Get all clubs ----------------
@tables.route('/clubs', methods=['GET'])
def get_all_clubs():
    query = '''
        SELECT id, name, type, subject, size
        FROM club
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response