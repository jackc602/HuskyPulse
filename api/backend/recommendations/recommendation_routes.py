from flask import Blueprint, jsonify, request
from backend.db_connection import db

recommendations = Blueprint('recommendations', __name__)

@recommendations.route('/recommendations', methods=['GET'])
def get_recommendations():
    student_id = request.args.get('applicant_id')
    cursor = db.get_db().cursor()

    # Get club types/subjects student has applied to
    interest_query = '''
        SELECT DISTINCT c.type, c.subject
        FROM application a
        JOIN club c ON a.club_id = c.id
        WHERE a.applicant_id = %s
    '''
    cursor.execute(interest_query, (student_id,))
    interests = cursor.fetchall()

    if not interests:
        return jsonify([])

    types = tuple(i['type'] for i in interests)
    subjects = tuple(i['subject'] for i in interests)

    # Recommend clubs that match any of those types/subjects
    rec_query = '''
        SELECT * FROM club
        WHERE type IN %s OR subject IN %s
    '''
    cursor.execute(rec_query, (types, subjects))
    recommendations = cursor.fetchall()
    return jsonify(recommendations)