from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from backend.db_connection import db

event = Blueprint("event", __name__)

# create an event in the database
@event.route("/event", methods = ["POST"])
def create_event():
    data = request.json
    query = """
    INSERT INTO event (name, start_date, end_date, location_id, club_id)
    VALUES (%s, %s, %s, %s, %s)
    """
    params = (data["name"], data["start_date"], data["end_date"], 
              data["location_id"], data["club_id"])
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    response = make_response("Successfully created new event")
    response.status_code = 200
    return response

# Get all events had by a certain club
@event.route("/club", methods = ["GET"])
def get_events():
    daclub_id = request.args.get("club_id")
    query = """
    SELECT * 
    FROM event e JOIN location l
    ON e.location_id = l.id
    WHERE club_id = %s
    """
    params = (daclub_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# Get a certain event based on id
@event.route("", methods = ["GET"])
def get_single_event():
    event_id = request.args.get("event_id")
    query = """
    SELECT *
    FROM event e
    WHERE e.id = %s
    """
    params = (event_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# Update an event in the database based on event id
@event.route("/update", methods = ["POST"])
def update_event():
    event_data = request.json
    query = """
    UPDATE event
    SET name = %s, start_date = %s, end_date = %s, location_id = %s
    WHERE event.id = %s
    """
    params = (event_data["name"], event_data["start_date"], event_data["end_date"], 
              event_data["location_id"], event_data["event_id"])
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    response = make_response("Successfully updated event")
    response.status_code = 200
    return response

# delete an event in the database
@event.route("/delete", methods = ["DELETE"])
def delete_event():
    data = request.json
    query = """
    DELETE FROM event 
    WHERE id = %s
    """
    params = (data["event_id"])
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    response = make_response(f"Successfully deleted event {data['event_id']}")
    response.status_code = 200
    return response
