import os
from functools import wraps
from flask import Blueprint, render_template, send_from_directory, current_app, session, redirect, url_for
from models.report import ReportModel
from models.evidence import EvidenceModel

views_bp = Blueprint('views', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('views.login'))
        return f(*args, **kwargs)
    return decorated_function

@views_bp.route('/')
def index():
    return render_template('index.html')

@views_bp.route('/login')
@views_bp.route('/signin')
def login():
    if 'user_id' in session:
        return redirect(url_for('views.dashboard'))
    return render_template('login.html')

@views_bp.route('/register')
@views_bp.route('/signup')
def register():
    if 'user_id' in session:
        return redirect(url_for('views.dashboard'))
    return render_template('register.html')

@views_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.index'))

@views_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@views_bp.route('/evidence')
@login_required
def evidence():
    return render_template('evidence.html')

@views_bp.route('/report')
@login_required
def report():
    return render_template('report.html')

@views_bp.route('/report/view/<int:report_id>')
@login_required
def report_view(report_id):
    report = ReportModel.get_by_id(report_id)
    if not report:
        return render_template('404.html'), 404
    evidence_items = EvidenceModel.get_all_by_user(report.get('user_id', 1))
    return render_template('report_view.html', report=report, evidence_items=evidence_items)

@views_bp.route('/emergency')
@login_required
def emergency():
    return render_template('emergency.html')

@views_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@views_bp.route('/about')
def about():
    return render_template('about.html')

# Static & Public Asset Helpers
@views_bp.route('/public/<path:filename>')
def serve_public(filename):
    public_dir = os.path.abspath(os.path.join(current_app.root_path, '../frontend/public'))
    return send_from_directory(public_dir, filename)

@views_bp.route('/favicon.ico')
def favicon():
    public_dir = os.path.abspath(os.path.join(current_app.root_path, '../frontend/public'))
    return send_from_directory(public_dir, 'favicon.ico')

@views_bp.route('/logo.png')
def logo():
    public_dir = os.path.abspath(os.path.join(current_app.root_path, '../frontend/public'))
    return send_from_directory(public_dir, 'logo.png')
