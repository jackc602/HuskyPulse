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
            WHERE applicant_id = ?
        '''
        cursor.execute(query, (applicant_id,))
    else:
        cursor.execute('SELECT * FROM application')

    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return jsonify([dict(zip(columns, row)) for row in results])


@application_routes.route('/application/club/<int:club_id>', methods=['GET'])
def applications_by_club(club_id):
    cursor = db.get_db().cursor()
    cursor.execute("SELECT id, club_id, status, applicant_id FROM application WHERE club_id = %s", (club_id,))
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    return (rows)


@application_routes.route('/application/update', methods=['POST'])
def update_application():
    data = request.json
    application_id = data.get('application_id')
    new_status = data.get('status')
    club_id = data.get('club_id')
    applicant_id = data.get('applicant_id')

    if not all([application_id, new_status, club_id, applicant_id]):
        return jsonify({'error': 'Missing fields'}), 400

    cursor = db.get_db().cursor()
    cursor.execute("""
        UPDATE application 
        SET status = ?, club_id = ?, applicant_id = ? 
        WHERE id = ?
    """, (new_status, club_id, applicant_id, application_id))
    db.get_db().commit()
    return jsonify({'message': 'Application updated successfully'}), 200


@application_routes.route('/other', methods=['GET'])
def get_applications_by_club():
    club_id = request.args.get("club_id")

    if not club_id:
        return jsonify({'error': 'Missing club_id'}), 400

    query = """
        SELECT a.*, s.*
        FROM application a
        JOIN student s ON s.id = a.applicant_id
        WHERE a.club_id = ?
    """
    cursor = db.get_db().cursor()
    cursor.execute(query, (club_id,))
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]

    return jsonify(result), 200
