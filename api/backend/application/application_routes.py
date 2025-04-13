from flask import Blueprint, jsonify, request
from backend.db_connection import db

application_routes = Blueprint('application_routes', __name__)

@application_routes.route('/applications', methods=['GET'])
def get_applications_by_query():
    applicant_id = request.args.get('applicant_id')
    cursor = db.get_db().cursor()

    if applicant_id:
        query = '''
            SELECT * FROM application
            WHERE applicant_id = %s
        '''
        cursor.execute(query, (applicant_id,))
    else:
        cursor.execute('SELECT * FROM application')

    results = cursor.fetchall()
    return jsonify(results)