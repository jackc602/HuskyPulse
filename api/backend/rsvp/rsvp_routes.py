from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from backend.db_connection import db

rsvp = Blueprint("rsvps", __name__)

# To get the rsvp information from students for an event
@rsvp.route('/event', methods=['GET'])
def get_rsvps():
    event_id = request.args.get("event_id")
    query = '''
        SELECT s.first_name, s.last_name, s.email, se.when_rsvped
        FROM event e JOIN student_event se ON se.event_id = e.id
        JOIN student s ON se.NUID = s.NUID
        WHERE e.id = %s
    '''
    params = (event_id, )
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# to get the event_id and NUID from student_event
@rsvp.route('/insert_rsvp', methods=['POST'])
def insert_rsvp():
    data = request.json
    query = """
    INSERT INTO student_event (NUID, event_id)
    VALUES (%s, %s)
    """
    params = (data["NUID"], data["event_id"])
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    response = make_response("Successfully created RSVP instance")
    response.status_code = 200
    return response