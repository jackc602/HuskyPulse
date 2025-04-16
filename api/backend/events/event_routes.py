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
    INSERT INTO event (id, name, start_date, end_date, location_id, club_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (data["id"], data["name"], data["start_date"], data["end_date"], 
              data["location_id"], data["club_id"])
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    response = make_response("Successfully created new event")
    response.status_code = 200
    return response

