from flask import Blueprint, request, jsonify
from db import get_db_connection

bp = Blueprint("charlie", __name__)


@bp.route("/recommendations", methods=["GET"])
def get_club_recommendations():
    nuid = request.args.get("nuid", type=int)

    if not nuid:
        return jsonify({"error": "Missing or invalid NUID"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Get student's interests (e.g., 'music', 'finance', 'outdoors')
    cursor.execute("""
        SELECT interest
        FROM student_interests
        WHERE nuid = %s
    """, (nuid,))
    interests = [row["interest"] for row in cursor.fetchall()]

    if not interests:
        return jsonify([]), 200

    # Match clubs with overlapping tags
    cursor.execute("""
        SELECT DISTINCT c.id, c.name, c.description
        FROM clubs c
        JOIN club_tags ct ON c.id = ct.club_id
        WHERE ct.tag = ANY(%s)
        LIMIT 10
    """, (interests,))

    clubs = cursor.fetchall()
    conn.close()

    recommendations = [{
        "club_id": row["id"],
        "club_name": row["name"],
        "description": row["description"]
    } for row in clubs]

    return jsonify(recommendations), 200
