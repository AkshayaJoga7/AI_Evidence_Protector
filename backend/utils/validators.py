import re

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_email(email: str) -> bool:
    """Validate email format using regex."""
    if not email:
        return False
    return bool(re.match(EMAIL_REGEX, email))

def validate_required_fields(data: dict, required_fields: list) -> tuple[bool, str]:
    """Check if all required fields are present in data dictionary."""
    if not data:
        return False, "Missing payload"
    missing = [field for field in required_fields if field not in data or data[field] is None or data[field] == ""]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, ""

def is_allowed_file(filename: str, allowed_extensions: set) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
