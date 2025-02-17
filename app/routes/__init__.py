from .user_routes import user_bp
from .auth_routes import auth_bp
from .event_routes import event_bp
from .comment_routes import comments_bp
from .educator_routes import educator_bp

def register_routes(app):
    # Регистрация маршрутов
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(event_bp, url_prefix='/api')
    app.register_blueprint(comments_bp, url_prefix='/api')
    app.register_blueprint(educator_bp, url_prefix='/api')
    app.register_blueprint(user_bp)