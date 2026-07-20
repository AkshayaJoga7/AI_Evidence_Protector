import os
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from config import config_by_name, Config
import database

def create_app(config_name='dev'):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.abspath(os.path.join(base_dir, '../frontend/templates'))
    static_dir = os.path.abspath(os.path.join(base_dir, '../frontend/static'))

    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir,
        instance_relative_config=True
    )
    
    # Load Configuration
    app.config.from_object(config_by_name.get(config_name, Config))
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize Database
    database.init_app(app)
    with app.app_context():
        database.init_db()

    # Ensure Upload Directories Exist
    os.makedirs(Config.IMAGE_UPLOADS, exist_ok=True)
    os.makedirs(Config.AUDIO_UPLOADS, exist_ok=True)
    os.makedirs(Config.REPORT_UPLOADS, exist_ok=True)

    # Register Blueprints
    from routes.views import views_bp
    from routes.auth import auth_bp
    from routes.emergency import emergency_bp
    from routes.evidence import evidence_bp
    from routes.report import report_bp
    from routes.ai import ai_bp

    # Frontend Views Blueprint (renders HTML templates at root & page paths)
    app.register_blueprint(views_bp)

    # Backend REST API Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(emergency_bp, url_prefix='/api/emergency')
    app.register_blueprint(evidence_bp, url_prefix='/api/evidence')
    app.register_blueprint(report_bp, url_prefix='/api/report')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "service": "AI Evidence Protector"}), 200

    # Custom Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        if request.path.startswith('/api/'):
            return jsonify({"error": "Resource not found", "status_code": 404}), 404
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        if request.path.startswith('/api/'):
            return jsonify({"error": "Internal server error", "status_code": 500}), 500
        return render_template('500.html'), 500

    return app

app = create_app(os.getenv('FLASK_ENV', 'dev'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
