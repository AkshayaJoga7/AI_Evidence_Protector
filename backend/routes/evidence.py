from flask import Blueprint, request
from models.evidence import EvidenceModel
from services.storage_service import StorageService
from services.ai_service import AIService
from utils.helpers import success_response, error_response
from utils.validators import is_allowed_file
from config import Config

evidence_bp = Blueprint('evidence', __name__)

@evidence_bp.route('/upload', methods=['POST'])
def upload_evidence():
    if 'file' not in request.files:
        return error_response("No file attached in request", 400)

    file = request.files['file']
    user_id = request.form.get('user_id')
    title = request.form.get('title', file.filename)
    file_type = request.form.get('file_type', 'image') # 'image' or 'audio'
    lat = request.form.get('latitude')
    lng = request.form.get('longitude')

    if not user_id:
        return error_response("user_id is required", 400)

    if file_type == 'image':
        allowed = Config.ALLOWED_IMAGE_EXTENSIONS
    else:
        allowed = Config.ALLOWED_AUDIO_EXTENSIONS

    if not is_allowed_file(file.filename, allowed):
        return error_response(f"Unsupported file format for {file_type}", 400)

    # Store file & compute digital hash signature
    upload_res = StorageService.save_upload(file, file_type)

    # Initial AI analysis
    ai_res = AIService.analyze_evidence(upload_res['file_path'], upload_res['file_hash'])

    evidence_id = EvidenceModel.create_evidence(
        user_id=user_id,
        title=title,
        file_type=file_type,
        file_path=upload_res['file_path'],
        file_hash=upload_res['file_hash'],
        latitude=lat,
        longitude=lng,
        ai_summary=ai_res['summary'],
        tamper_status=ai_res['status']
    )

    return success_response(
        data={
            "evidence_id": evidence_id,
            "title": title,
            "file_type": file_type,
            "file_hash": upload_res['file_hash'],
            "tamper_status": ai_res['status'],
            "ai_summary": ai_res['summary']
        },
        message="Evidence uploaded and secured with cryptographic hash",
        status_code=201
    )

@evidence_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_evidence(user_id):
    items = EvidenceModel.get_all_by_user(user_id)
    return success_response(data=items, message=f"Retrieved {len(items)} evidence item(s)")

@evidence_bp.route('/<int:evidence_id>', methods=['GET'])
def get_evidence(evidence_id):
    item = EvidenceModel.get_by_id(evidence_id)
    if not item:
        return error_response("Evidence item not found", 404)
    return success_response(data=item)
