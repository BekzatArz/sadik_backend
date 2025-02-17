from flask import Blueprint, request, jsonify
from app.services.user_service import get_user
from app.services.db_service import get_server_version

user_bp = Blueprint('users', __name__)

@user_bp.route('/users', methods=['POST'])
def add_user():
    data = request.json
    return jsonify(user), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def fetch_user(user_id):
    user = get_user(user_id)
    return jsonify(user)

@user_bp.route('/db/version', methods=['GET'])
def get_db_version():
    version = get_server_version()
    return jsonify({"db_version": version})
