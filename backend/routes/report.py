from flask import Blueprint, request, send_file
from models.report import ReportModel
from models.evidence import EvidenceModel
from services.report_service import ReportService
from utils.helpers import success_response, error_response
from utils.validators import validate_required_fields
import os

report_bp = Blueprint('report', __name__)

@report_bp.route('/create', methods=['POST'])
def create_report():
    data = request.get_json()
    valid, msg = validate_required_fields(data, ['user_id', 'title', 'description'])
    if not valid:
        return error_response(msg, 400)

    report_id = ReportModel.create_report(
        user_id=data['user_id'],
        title=data['title'],
        description=data['description'],
        status='draft'
    )

    evidence_items = EvidenceModel.get_all_by_user(data['user_id'])
    report_file = ReportService.generate_pdf_report(
        {"id": report_id, "title": data['title'], "description": data['description'], "status": "draft"},
        evidence_items
    )

    ReportModel.update_status(report_id, status='generated', report_file_path=report_file)

    return success_response(
        data={
            "report_id": report_id,
            "title": data['title'],
            "status": "generated",
            "report_file": report_file
        },
        message="Incident report generated successfully",
        status_code=201
    )

@report_bp.route('/user/<int:user_id>', methods=['GET'])
def list_user_reports(user_id):
    reports = ReportModel.get_all_by_user(user_id)
    return success_response(data=reports)

@report_bp.route('/download/<int:report_id>', methods=['GET'])
def download_report(report_id):
    report = ReportModel.get_by_id(report_id)
    if not report or not report.get('report_file_path'):
        return error_response("Report file not found", 404)

    file_path = report['report_file_path']
    if not os.path.exists(file_path):
        return error_response("Report file missing on server", 404)

    return send_file(file_path, as_attachment=True)
