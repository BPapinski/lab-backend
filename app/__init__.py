from flask import Flask
from flask_login import LoginManager
from .models import db, User
import os

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='../static')
    app.secret_key = os.environ.get('APP_SECRET', 'dev-secret-key-change-in-prod')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .controllers import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app