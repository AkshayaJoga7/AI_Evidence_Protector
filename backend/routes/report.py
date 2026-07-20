import os
from flask import Blueprint, request, send_file, session, render_template
from models.report import ReportModel
from models.evidence import EvidenceModel
from services.report_service import ReportService
from utils.helpers import success_response, error_response
from utils.validators import validate_required_fields

report_bp = Blueprint('report', __name__)

@report_bp.route('/create', methods=['POST'])
def create_report():
    data = request.get_json() or {}
    
    title = data.get('title')
    description = data.get('description')
    user_id = data.get('user_id') or session.get('user_id') or 1

    if not title or not description:
        return error_response("Title and Description are required", 400)

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        user_id = 1

    report_id = ReportModel.create_report(
        user_id=user_id,
        title=title,
        description=description,
        status='generated'
    )

    evidence_items = EvidenceModel.get_all_by_user(user_id)
    report_file = ReportService.generate_pdf_report(
        {"id": report_id, "title": title, "description": description, "status": "generated"},
        evidence_items
    )

    ReportModel.update_status(report_id, status='generated', report_file_path=report_file)

    return success_response(
        data={
            "report_id": report_id,
            "title": title,
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

@report_bp.route('/view/<int:report_id>', methods=['GET'])
def view_report(report_id):
    report = ReportModel.get_by_id(report_id)
    if not report:
        return error_response("Report not found", 404)

    evidence_items = EvidenceModel.get_all_by_user(report.get('user_id', 1))
    return render_template('report_view.html', report=report, evidence_items=evidence_items)

@report_bp.route('/download/<int:report_id>', methods=['GET'])
def download_report(report_id):
    report = ReportModel.get_by_id(report_id)
    if not report or not report.get('report_file_path'):
        return error_response("Report file not found", 404)

    file_path = report['report_file_path']
    if not os.path.exists(file_path):
        return error_response("Report file missing on server", 404)

    safe_title = "".join([c if c.isalnum() else "_" for c in report.get('title', 'report')])
    download_name = f"{safe_title}_# {report_id}.pdf"
    mimetype = "text/plain" if file_path.endswith('.txt') else "application/pdf"

    return send_file(
        file_path,
        as_attachment=True,
        download_name=download_name,
        mimetype=mimetype
    )
