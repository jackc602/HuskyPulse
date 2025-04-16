from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import db

location = Blueprint("location", __name__)

@location.route('/capacity', methods=['GET'])
def capacity():
    capacity = request.args.get("capacity")

    try:
        capacity = int(capacity)
    except (TypeError, ValueError):
        return make_response(jsonify({"error": "Invalid capacity value"}), 400)

    query = """
    SELECT *
    FROM location
    WHERE capacity > %s
    """
    params = (capacity,)
    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()


    response = make_response(jsonify(data))
    response.status_code = 200
    return response


@location.route('/location', methods=['GET'])
def get_all_():
    query = '''
        SELECT *
        FROM location
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response