from flask import Blueprint, request, jsonify, make_response
from datetime import datetime
from backend.db_connection import db

feedback = Blueprint('feedback', __name__)

# ---------------- Submit feedback ----------------
@feedback.route('/feedback', methods=['POST'])
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
@feedback.route('/feedbacks', methods=['GET'])
def get_all_feedback():
    query = '''
        SELECT *
        FROM feedback
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)