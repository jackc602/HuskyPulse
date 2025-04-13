from flask import Blueprint, request, jsonify, make_response
from datetime import datetime
from backend.db_connection import db

# making one blueprint for both clubs and feedback
tables = Blueprint('tables', __name__)  

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


# ---------------- Submit feedback ----------------
@tables.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    recipient_id = data['recipient_id']
    recipient_type = data['recipient_type']
    sender_id = data['sender_id']
    sender_type = data['sender_type']
    content = data['content']
    date_submitted = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    query = '''
        INSERT INTO feedback (recipient_id, recipient_type, sender_id, sender_type, content, date_submitted)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (recipient_id, recipient_type, sender_id, sender_type, content, date_submitted))
    db.get_db().commit()

    return make_response(jsonify({"message": "Feedback submitted successfully!"}), 201)


# route to get all feedback from the feedback table
@tables.route('/feedbacks', methods=['GET'])
def get_all_feedback():
    query = '''
        SELECT *
        FROM feedback
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)