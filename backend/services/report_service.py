import os
from config import Config
from datetime import datetime

class ReportService:
    @staticmethod
    def generate_pdf_report(report_data: dict, evidence_list: list) -> str:
        """
        Generates formatted evidence summary report text/markdown or PDF.
        """
        reports_dir = Config.REPORT_UPLOADS
        os.makedirs(reports_dir, exist_ok=True)

        report_id = report_data.get('id', 'new')
        filename = f"report_{report_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        file_path = os.path.join(reports_dir, filename)

        content = f"""==================================================
AI EVIDENCE PROTECTOR - OFFICIAL INCIDENT REPORT
==================================================
Report ID: {report_id}
Title: {report_data.get('title')}
Generated At: {datetime.utcnow().isoformat()} UTC
Status: {report_data.get('status')}

INCIDENT DESCRIPTION:
---------------------
{report_data.get('description')}

ATTACHED EVIDENCE ({len(evidence_list)} item(s)):
---------------------
"""
        for idx, item in enumerate(evidence_list, start=1):
            content += f"""
[{idx}] Title: {item.get('title')}
    Type: {item.get('file_type')}
    SHA-256 Hash: {item.get('file_hash')}
    Location: Lat {item.get('latitude')}, Long {item.get('longitude')}
    Tamper Status: {item.get('tamper_status')}
    AI Notes: {item.get('ai_summary', 'N/A')}
"""

        content += "\n==================================================\nEND OF REPORT\n"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return file_path
