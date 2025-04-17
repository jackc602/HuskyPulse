from flask import Blueprint, jsonify, request, make_response
from backend.db_connection import db

application_routes = Blueprint('application_routes', __name__)

# Retrieve the applications made by a certain user
@application_routes.route('/applications', methods=['GET'])
def get_applications_by_query():
    applicant_id = request.args.get('applicant_id')
    cursor = db.get_db().cursor()

    if applicant_id:
        query = '''
            SELECT a.*, c.name as club_name
            FROM application a JOIN club c ON a.club_id = c.id
            WHERE applicant_id = %s
        '''
        cursor.execute(query, (applicant_id))
    else:
        cursor.execute('SELECT * FROM application')

    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@application_routes.route('/application/club/<int:club_id>', methods=['GET'])
def applications_by_club(club_id):
    cursor = db.get_db().cursor()
    cursor.execute("""
                   SELECT a.id, a.club_id as club_id, a.status as status, a.applicant_id as applicant_id,
                   s.*
                   FROM application a join student s on a.applicant_id = s.nuid
                   WHERE club_id = %s"""
                   , (club_id,))
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    return (rows)


@application_routes.route('/application/apply', methods=['POST'])
def post_application():
    data = request.json
    query = '''
        INSERT INTO application (club_id, status, applicant_id)
        VALUES (%s, %s, %s)
    '''
    params = (data["club_id"], data["status"], data["applicant_id"])
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    response = make_response("Successfully created new application")
    response.status_code = 200
    return response
    

@application_routes.route('/application/update', methods=['PUT'])
def update_application():
    data = request.json
    query = '''
        UPDATE application
        SET status = %s
        WHERE id = %s
    '''
    params = (data["status"], data["id"])
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    response = make_response("Successfully updated application")
    response.status_code = 200
    return response
