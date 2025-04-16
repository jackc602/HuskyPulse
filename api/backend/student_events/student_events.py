from flask import Blueprint, jsonify
from backend.db_connection import db

student_events = Blueprint("student_events", __name__)

@student_events.route('/all_event_rsvps', methods=['GET'])
def get_all_event_rsvps():
    query = '''
        SELECT 
            e.name AS event_name,
            e.start_date,
            e.end_date,
            e.id,
            l.building,
            l.room_num
        FROM event e JOIN location l ON e.location_id = l.id
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return jsonify(data), 200






