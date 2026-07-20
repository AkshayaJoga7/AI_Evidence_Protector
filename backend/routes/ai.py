from flask import Blueprint, request
from models.evidence import EvidenceModel
from services.ai_service import AIService
from utils.helpers import success_response, error_response

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/verify-tamper/<int:evidence_id>', methods=['POST'])
def verify_tamper(evidence_id):
    item = EvidenceModel.get_by_id(evidence_id)
    if not item:
        return error_response("Evidence item not found", 404)

    analysis = AIService.analyze_evidence(item['file_path'], item['file_hash'])
    
    EvidenceModel.update_tamper_status(
        evidence_id=evidence_id,
        status=analysis['status'],
        ai_summary=analysis['summary']
    )

    return success_response(
        data={
            "evidence_id": evidence_id,
            "status": analysis['status'],
            "summary": analysis['summary'],
            "authentic": analysis['authentic']
        },
        message="AI verification completed"
    )

@ai_bp.route('/summarize/<int:evidence_id>', methods=['GET'])
def get_ai_summary(evidence_id):
    item = EvidenceModel.get_by_id(evidence_id)
    if not item:
        return error_response("Evidence item not found", 404)

    return success_response(
        data={
            "evidence_id": evidence_id,
            "title": item['title'],
            "ai_summary": item.get('ai_summary', 'No summary generated yet.'),
            "tamper_status": item.get('tamper_status', 'unverified')
        }
    )
