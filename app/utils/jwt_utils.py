import jwt
import datetime
from flask import current_app

def create_jwt_token(user_or_admin, role):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    
    payload = {
        'sub': str(user_or_admin.id),
        'role': role, 
        'exp': expiration_time
    }
    
    # Преобразуем в строку, если jwt.encode возвращает bytes
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token.decode('utf-8') if isinstance(token, bytes) else token  # Преобразуем в строку, если это bytes


def decode_jwt_token(token):
    try:
        # Исправленный параметр algorithms в decode
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}
    except jwt.InvalidTokenError as e:
        return {'error': f'Invalid token: {str(e)}'}
