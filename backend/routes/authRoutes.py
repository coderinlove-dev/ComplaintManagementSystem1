# routes/authRoutes.py
from flask import Blueprint, request, jsonify
from controllers.authController import loginUser, registerUser
import jwt, os
from datetime import datetime, timedelta

auth_bp = Blueprint("auth_bp", __name__)

# --- Ensure JWT_SECRET exists ---
JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError("❌ JWT_SECRET environment variable is missing! Set it in Railway variables.")

# --- Register endpoint ---
@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        # Call controller function
        return registerUser()
    except Exception as e:
        print("REGISTER ERROR:", e)  # This will show in Railway logs
        return jsonify({"message": "Server error"}), 500

# --- Login endpoint ---
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        # Call controller function
        return loginUser()
    except Exception as e:
        print("LOGIN ERROR:", e)  # This will show in Railway logs
        return jsonify({"message": "Server error"}), 500

# --- Refresh token endpoint ---
@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    try:
        data = request.get_json()
        refresh_token = data.get("refresh_token")
        if not refresh_token:
            return jsonify({"message": "Refresh token missing"}), 400

        payload = jwt.decode(refresh_token, JWT_SECRET, algorithms=["HS256"])
        new_access_token = jwt.encode(
            {
                "id": payload["id"],
                "role": payload["role"],
                "exp": datetime.utcnow() + timedelta(minutes=30)
            },
            JWT_SECRET,
            algorithm="HS256"
        )

        return jsonify({"access_token": new_access_token}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Refresh token expired, please login again"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid refresh token"}), 401
    except Exception as e:
        print("REFRESH TOKEN ERROR:", e)
        return jsonify({"message": "Server error"}), 500
