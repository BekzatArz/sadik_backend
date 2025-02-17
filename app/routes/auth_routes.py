from flask import Blueprint, request, jsonify
from app.models import User, Admin
from app.services.auth_service import create_user, create_admin
from werkzeug.security import check_password_hash
from app.utils.auth import create_jwt_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    if not data.get('first_name') or not data.get('last_name') or not data.get('phone_number') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing data"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email is already in use"}), 400
    
    if User.query.filter_by(phone_number=data['phone_number']).first():
        return jsonify({"error": "Phone number is already in use"}), 400
    
    create_user(data)

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing data"}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_jwt_token(user, 'user')
    print(user.id)
    return jsonify({
        "message": "Login successful",
        "token": token,
        }), 200
    
@auth_bp.route('/register-admin', methods=['POST'])
def register_admin():
    data = request.get_json()
    if not data.get('company_name') or not data.get('phone_number') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing data"}), 400

    if Admin.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email is already in use"}), 400
    
    if Admin.query.filter_by(phone_number=data['phone_number']).first():
        return jsonify({"error": "Phone number is already in use"}), 400
    
    if Admin.query.filter_by(company_name=data['company_name']).first():
        return jsonify({'error': "Company name is already in use"}), 400

    create_admin(data)

    return jsonify({"message": "Admin registered successfully"}), 201


@auth_bp.route('/login-admin', methods=['POST'])
def login_admin():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing data"}), 400

    admin = Admin.query.filter_by(email=data['email']).first()

    if not admin or not admin.check_password(data['password']):
        return jsonify({"error": "Invalid credentials"}), 401
    
    if not admin.is_verified:
        return jsonify({"error": 'Admin account is not verified'}), 403

    token = create_jwt_token(admin, 'admin')
    return jsonify({
        "message": "Login successful",
        "token": token
        }), 200
    