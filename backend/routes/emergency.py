from flask import Blueprint, request
from database import get_db
from utils.helpers import success_response, error_response
from utils.validators import validate_required_fields

emergency_bp = Blueprint('emergency', __name__)

@emergency_bp.route('/trigger', methods=['POST'])
def trigger_sos():
    data = request.get_json()
    valid, msg = validate_required_fields(data, ['user_id', 'latitude', 'longitude'])
    if not valid:
        return error_response(msg, 400)

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO emergency_alerts (user_id, latitude, longitude, status)
        VALUES (?, ?, ?, 'active')
        """,
        (data['user_id'], data['latitude'], data['longitude'])
    )
    db.commit()
    alert_id = cursor.lastrowid

    return success_response(
        data={
            "alert_id": alert_id,
            "user_id": data['user_id'],
            "latitude": data['latitude'],
            "longitude": data['longitude'],
            "status": "active"
        },
        message="SOS Emergency Alert Triggered Successfully!",
        status_code=201
    )

@emergency_bp.route('/resolve/<int:alert_id>', methods=['POST'])
def resolve_sos(alert_id):
    db = get_db()
    db.execute(
        "UPDATE emergency_alerts SET status = 'resolved' WHERE id = ?",
        (alert_id,)
    )
    db.commit()
    return success_response(message=f"Emergency Alert {alert_id} resolved")
