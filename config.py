import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')


class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-insecure-flask-secret-key-replace-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 5
    WTF_CSRF_ENABLED = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max payload

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{BASE_DIR / 'instance' / 'blog.db'}"


class TestingConfig(Config):
    """Testing configuration with in-memory SQLite and disabled CSRF."""
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{BASE_DIR / 'instance' / 'blog.db'}"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
