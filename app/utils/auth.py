from functools import wraps
from flask import request, jsonify
from app.models import User, Admin
from app.utils.jwt_utils import create_jwt_token, decode_jwt_token
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'error': 'Token is missing'}), 403

        payload = decode_jwt_token(token)
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 403

        # Определяем роль пользователя из payload
        role = payload.get('role')
        
        if role == 'user':
            current_user = User.query.get(payload['sub'])
            if not current_user:
                return jsonify({'error': 'User not found'}), 404
            return f(current_user, *args, **kwargs)
        
        elif role == 'admin':
            current_admin = Admin.query.get(payload['sub'])
            if not current_admin:
                return jsonify({'error': 'Admin not found'}), 404
            return f(current_admin, *args, **kwargs)

        # Если роль не определена
        return jsonify({'error': 'Invalid role'}), 403

    return decorated_function