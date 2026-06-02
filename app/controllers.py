from flask import (
    Blueprint, render_template, redirect, url_for,
    request, flash, send_from_directory, session
)
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User

main = Blueprint('main', __name__)

SUPPORTED_LANGS = ['pl', 'en']


def _t(key_path: str, default: str = '') -> str:
    """Return a translated string for the current session language.

    key_path uses dot notation, e.g. 'register.error_username'.
    Used in controller code (flash messages) where the Jinja2 context
    is not yet available.
    """
    from flask import current_app
    lang = session.get('lang', 'pl')
    from app import load_translations
    translations = load_translations(lang)
    parts = key_path.split('.')
    node = translations
    for part in parts:
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return default
    return str(node)


# ---------------------------------------------------------------------------
# Language switcher
# ---------------------------------------------------------------------------

@main.route('/set-lang/<lang>')
def set_lang(lang):
    if lang in SUPPORTED_LANGS:
        session['lang'] = lang
    referrer = request.referrer
    return redirect(referrer if referrer else url_for('main.index'))


# ---------------------------------------------------------------------------
# Public routes
# ---------------------------------------------------------------------------

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/privacy')
def privacy():
    return render_template('privacy.html')


@main.route('/download')
def download():
    return send_from_directory('../static', 'code.zip', as_attachment=True)


# ---------------------------------------------------------------------------
# Auth routes
# ---------------------------------------------------------------------------

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        if User.query.filter_by(username=username).first():
            flash(_t('register.error_username', 'Nazwa użytkownika jest już zajęta.'), 'error')
        elif User.query.filter_by(email=email).first():
            flash(_t('register.error_email', 'Ten adres e-mail jest już zarejestrowany.'), 'error')
        elif len(password) < 6:
            flash(_t('register.error_password', 'Hasło musi mieć co najmniej 6 znaków.'), 'error')
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('main.dashboard'))
    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash(_t('login.error_invalid', 'Nieprawidłowa nazwa użytkownika lub hasło.'), 'error')
    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
