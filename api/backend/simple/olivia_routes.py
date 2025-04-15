from flask import Blueprint, request, jsonify
from backend.db_connection import db



bp = Blueprint("olivia", __name__)


# 3.1 - Manage user roles
@bp.route("/admin/assign-role", methods=["POST"])
def assign_role():
    try:
        data = request.get_json()
        admin_id = data.get("admin_id")
        role_name = data.get("role_name")

        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO role (admin_id, role_name)
            VALUES (%s, %s)
        """, (admin_id, role_name))
        conn.commit()
        conn.close()

        return jsonify({"message": "Role assigned successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 3.2 - Log compliance update
@bp.route("/admin/compliance", methods=["POST"])
def log_compliance():
    data = request.get_json()
    status = data.get("status")
    admin_id = data.get("admin_id")
    club_id = data.get("club_id")

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO compliance (status, admin_id, club_id)
        VALUES (%s, %s, %s)
    """, (status, admin_id, club_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Compliance status logged."}), 201


# 3.3, 3.6 - Log admin actions
@bp.route("/admin/log", methods=["POST"])
def log_action():
    data = request.get_json()
    admin_id = data.get("admin_id")
    content = data.get("content")

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO logs (admin_id, content)
        VALUES (%s, %s)
    """, (admin_id, content))
    conn.commit()
    conn.close()

    return jsonify({"message": "Action logged successfully"}), 201


# 3.4 - Log a backup
@bp.route("/admin/backup", methods=["POST"])
def backup_data():
    data = request.get_json()
    admin_id = data.get("admin_id")
    content = data.get("content")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO backup (admin_id, content)
        VALUES (%s, %s)
    """, (admin_id, content))
    conn.commit()
    conn.close()

    return jsonify({"message": "Backup logged successfully"}), 201
