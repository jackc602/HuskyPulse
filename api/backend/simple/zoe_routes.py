from flask import Blueprint, request, jsonify

bp = Blueprint("zoe", __name__)

# Route 1: Create a new event (POST)
@bp.route('/api/events', methods=['POST'])
def create_event():
    """
    This route handles creation of a new event.
    Expected input: JSON with keys: name, start_date, end_date, location_id, club_id
    """
    data = request.get_json()
    name = data.get("name")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    location_id = data.get("location_id")
    club_id = data.get("club_id")

    # Log info (simulating DB write)
    print(
        f"[CREATE EVENT] name={name}, start={start_date}, end={end_date}, location_id={location_id}, club_id={club_id}")

    return jsonify({"message": f"Event '{name}' created successfully"}), 201

# Route 2: Get RSVP count for an event (GET)
@bp.route('/api/events/<int:event_id>/rsvps', methods=['GET'])
def get_event_rsvp(event_id):
    """
    This route returns the number of RSVPs for a given event.
    """
    mock_rsvp_count = 42
    print(f"[GET RSVP COUNT] for event_id={event_id} → count={mock_rsvp_count}")

    return jsonify({
        "event_id": event_id,
        "rsvp_count": mock_rsvp_count
    }), 200
