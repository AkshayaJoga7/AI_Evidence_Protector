import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import config_by_name, Config
import database

def create_app(config_name='dev'):
    app = Flask(__name__, instance_relative_config=True)
    
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
    from routes.auth import auth_bp
    from routes.emergency import emergency_bp
    from routes.evidence import evidence_bp
    from routes.report import report_bp
    from routes.ai import ai_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(emergency_bp, url_prefix='/api/emergency')
    app.register_blueprint(evidence_bp, url_prefix='/api/evidence')
    app.register_blueprint(report_bp, url_prefix='/api/report')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            "service": "AI Evidence Protector API",
            "status": "online",
            "version": "1.0.0",
            "endpoints": {
                "auth": "/api/auth",
                "emergency": "/api/emergency",
                "evidence": "/api/evidence",
                "report": "/api/report",
                "ai": "/api/ai"
            }
        })

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy"}), 200

    return app

app = create_app(os.getenv('FLASK_ENV', 'dev'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
