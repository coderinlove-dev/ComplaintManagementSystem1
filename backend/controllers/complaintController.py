# controllers/complaint_controller.py

from flask import request, jsonify, g
from config.db import get_connection
import os

# =========================================================
# ADD NEW COMPLAINT
# =========================================================
def addComplaint():
    try:
        # 1️⃣ Get logged-in user ID from JWT
        user_id = g.user["id"]

        # 2️⃣ Read form fields (MUST match DB columns)
        subject = request.form.get("subject")
        type_ = request.form.get("type")
        description = request.form.get("description")

        # 3️⃣ Validate required fields (PREVENTS 500)
        if not subject or not type_ or not description:
            return jsonify({
                "message": "Subject, type, and description are required"
            }), 400

        # 4️⃣ Handle optional attachment
        attachment = None
        if "attachment" in request.files:
            file = request.files["attachment"]

            if file and file.filename:
                attachment = file.filename
                os.makedirs("uploads", exist_ok=True)
                file.save(os.path.join("uploads", attachment))

        # 5️⃣ Insert into Railway MySQL database
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO complaints
                (user_id, subject, type, description, attachment, status)
            VALUES
                (%s, %s, %s, %s, %s, %s)
            """,
            (user_id, subject, type_, description, attachment, "Unsolved")
        )

        conn.commit()
        cursor.close()
        conn.close()

        # 6️⃣ Success response
        return jsonify({
            "message": "Complaint submitted successfully!"
        }), 201

    except Exception as e:
        # 7️⃣ Clear error response (helps debugging)
        return jsonify({
            "message": "Could not submit complaint",
            "error": str(e)
        }), 500


# =========================================================
# GET USER'S UNSOLVED COMPLAINTS
# =========================================================
def getUserUnsolvedComplaints():
    try:
        user_id = g.user["id"]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                id,
                subject,
                type,
                description,
                attachment,
                status,
                created_at
            FROM complaints
            WHERE user_id = %s
              AND status = 'Unsolved'
            ORDER BY created_at DESC
            """,
            (user_id,)
        )

        complaints = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(complaints), 200

    except Exception as e:
        return jsonify({
            "message": "Unable to fetch complaints",
            "error": str(e)
        }), 500


# =========================================================
# GET USER'S SOLVED COMPLAINTS
# =========================================================
def getUserSolvedComplaints():
    try:
        user_id = g.user["id"]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                id,
                subject,
                type,
                description,
                attachment,
                status,
                created_at
            FROM complaints
            WHERE user_id = %s
              AND status = 'Solved'
            ORDER BY created_at DESC
            """,
            (user_id,)
        )

        complaints = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(complaints), 200

    except Exception as e:
        return jsonify({
            "message": "Unable to fetch solved complaints",
            "error": str(e)
        }), 500
