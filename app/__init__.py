from flask import Flask, session
from flask_login import LoginManager
from .models import db, User
import os
import json


def load_translations(lang: str) -> dict:
    """Load translation dict for the given language code.

    Falls back to Polish if the requested language file does not exist.
    Adding a new language is as simple as dropping a new JSON file into
    the translations/ directory and adding its code to the SUPPORTED_LANGS
    list in controllers.py.
    """
    translations_dir = os.path.join(os.path.dirname(__file__), 'translations')
    path = os.path.join(translations_dir, f'{lang}.json')
    if not os.path.exists(path):
        path = os.path.join(translations_dir, 'pl.json')
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='../static')
    app.secret_key = os.environ.get('APP_SECRET', 'dev-secret-key-change-in-prod')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Zaloguj się, aby uzyskać dostęp.'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_i18n():
        """Inject translation dict and current language into every template."""
        lang = session.get('lang', 'pl')
        return dict(t=load_translations(lang), lang=lang)

    from .controllers import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
