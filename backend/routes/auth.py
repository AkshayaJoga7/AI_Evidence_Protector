from flask import Blueprint, request, session
from models.user import UserModel
from utils.security import hash_password, verify_password, generate_api_token
from utils.helpers import success_response, error_response
from utils.validators import validate_email, validate_required_fields

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    valid, msg = validate_required_fields(data, ['username', 'email', 'password'])
    if not valid:
        return error_response(msg, 400)

    if not validate_email(data['email']):
        return error_response("Invalid email format", 400)

    if UserModel.get_by_email(data['email']):
        return error_response("Email already registered", 400)

    if UserModel.get_by_username(data['username']):
        return error_response("Username already taken", 400)

    pwd_hash = hash_password(data['password'])
    user_id = UserModel.create_user(
        username=data['username'],
        email=data['email'],
        password_hash=pwd_hash,
        full_name=data.get('full_name'),
        phone=data.get('phone')
    )

    token = generate_api_token()
    return success_response(
        data={"user_id": user_id, "username": data['username'], "token": token},
        message="User registered successfully! Please log in.",
        status_code=201
    )

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    valid, msg = validate_required_fields(data, ['email', 'password'])
    if not valid:
        return error_response(msg, 400)

    user = UserModel.get_by_email(data['email'])
    if not user or not verify_password(user['password_hash'], data['password']):
        return error_response("Invalid email or password", 401)

    token = generate_api_token()

    # Populate Flask encrypted session
    session['user_id'] = user['id']
    session['username'] = user['username']
    session['email'] = user['email']

    return success_response(
        data={
            "user_id": user['id'],
            "username": user['username'],
            "email": user['email'],
            "token": token
        },
        message="Login successful"
    )

@auth_bp.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return success_response(message="Logged out successfully")
