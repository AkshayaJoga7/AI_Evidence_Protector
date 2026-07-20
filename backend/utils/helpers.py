from flask import jsonify
from datetime import datetime

def success_response(data=None, message="Success", status_code=200):
    """Format standard JSON success response."""
    payload = {
        "success": True,
        "message": message
    }
    if data is not None:
        payload["data"] = data
    return jsonify(payload), status_code

def error_response(message="An error occurred", status_code=400, errors=None):
    """Format standard JSON error response."""
    payload = {
        "success": False,
        "error": message
    }
    if errors is not None:
        payload["details"] = errors
    return jsonify(payload), status_code

def get_iso_timestamp():
    """Return current timestamp in ISO 8601 format."""
    return datetime.utcnow().isoformat() + "Z"
