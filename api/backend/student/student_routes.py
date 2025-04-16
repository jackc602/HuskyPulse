from flask import Blueprint, request, jsonify, make_response
from datetime import datetime
from backend.db_connection import db

# making the blueprint for club
student = Blueprint('student', __name__)  

# ---------------- Get all students ----------------
@student.route('/student', methods=['GET'])
def get_all_students():
    query = '''
        SELECT *
        FROM student
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response