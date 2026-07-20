from database import get_db

class EvidenceModel:
    @staticmethod
    def create_evidence(user_id, title, file_type, file_path, file_hash, latitude=None, longitude=None, ai_summary=None, tamper_status='verified_authentic'):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO evidence (user_id, title, file_type, file_path, file_hash, latitude, longitude, ai_summary, tamper_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, title, file_type, file_path, file_hash, latitude, longitude, ai_summary, tamper_status)
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def get_by_id(evidence_id):
        db = get_db()
        item = db.execute("SELECT * FROM evidence WHERE id = ?", (evidence_id,)).fetchone()
        return dict(item) if item else None

    @staticmethod
    def get_all_by_user(user_id):
        db = get_db()
        rows = db.execute("SELECT * FROM evidence WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def update_tamper_status(evidence_id, status, ai_summary=None):
        db = get_db()
        if ai_summary:
            db.execute(
                "UPDATE evidence SET tamper_status = ?, ai_summary = ? WHERE id = ?",
                (status, ai_summary, evidence_id)
            )
        else:
            db.execute(
                "UPDATE evidence SET tamper_status = ? WHERE id = ?",
                (status, evidence_id)
            )
        db.commit()
