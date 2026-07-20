from database import get_db

class ReportModel:
    @staticmethod
    def create_report(user_id, title, description, status='draft', report_file_path=None):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO reports (user_id, title, description, status, report_file_path)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, title, description, status, report_file_path)
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def get_by_id(report_id):
        db = get_db()
        report = db.execute("SELECT * FROM reports WHERE id = ?", (report_id,)).fetchone()
        return dict(report) if report else None

    @staticmethod
    def get_all_by_user(user_id):
        db = get_db()
        rows = db.execute("SELECT * FROM reports WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def update_status(report_id, status, report_file_path=None):
        db = get_db()
        if report_file_path:
            db.execute(
                "UPDATE reports SET status = ?, report_file_path = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (status, report_file_path, report_id)
            )
        else:
            db.execute(
                "UPDATE reports SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (status, report_id)
            )
        db.commit()
