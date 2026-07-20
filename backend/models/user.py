from database import get_db

class UserModel:
    @staticmethod
    def create_user(username, email, password_hash, full_name=None, phone=None):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, full_name, phone)
            VALUES (?, ?, ?, ?, ?)
            """,
            (username, email, password_hash, full_name, phone)
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def get_by_email(email):
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return dict(user) if user else None

    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(user) if user else None

    @staticmethod
    def get_by_username(username):
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        return dict(user) if user else None
