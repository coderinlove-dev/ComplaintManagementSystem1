# routes/complaintRoutes.py

from flask import Blueprint
from controllers.complaint_controller import (
    addComplaint,
    getUserUnsolvedComplaints,
    getUserSolvedComplaints
)
from middleware.authMiddleware import authenticate_token

complaint_bp = Blueprint("complaint_bp", __name__)

# =========================================================
# Add new complaint (multipart/form-data)
# =========================================================
@complaint_bp.route("", methods=["POST"])
@authenticate_token
def create_complaint():
    # All form-data & files are handled in controller
    return addComplaint()

# =========================================================
# Get unsolved complaints for logged-in user
# =========================================================
@complaint_bp.route("/unsolved", methods=["GET"])
@authenticate_token
def unsolved_complaints():
    return getUserUnsolvedComplaints()

# =========================================================
# Get solved complaints for logged-in user
# =========================================================
@complaint_bp.route("/solved", methods=["GET"])
@authenticate_token
def solved_complaints():
    return getUserSolvedComplaints()
