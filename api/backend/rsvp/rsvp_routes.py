from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from backend.db_connection import db

rsvp = Blueprint("rsvps", __name__)

@rsvp.route('/rsvp', methods=['GET'])
def get_products():
    query = '''
        SELECT  NUID, 
                when_rsvped, 
                name, 
                start_date, 
                end_date,
                location_id
        FROM event e JOIN student_events se
        ON se.event_id = e.id
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response