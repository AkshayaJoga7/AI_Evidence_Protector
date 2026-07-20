import os

class Config:
    """Base Configuration Class for AI Evidence Protector Backend."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ai-evidence-protector-secret-key-2026')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Database Configuration
    DATABASE_PATH = os.environ.get(
        'DATABASE_PATH', 
        os.path.join(BASE_DIR, 'database', 'evidence.db')
    )
    
    # Upload Directories
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    IMAGE_UPLOADS = os.path.join(UPLOAD_FOLDER, 'images')
    AUDIO_UPLOADS = os.path.join(UPLOAD_FOLDER, 'audio')
    REPORT_UPLOADS = os.path.join(UPLOAD_FOLDER, 'reports')
    
    # Upload constraints
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB max limit
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'aac', 'm4a', 'ogg'}

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'default': DevelopmentConfig
}
