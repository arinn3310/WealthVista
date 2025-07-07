import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # API Keys
    ALPHA_VANTAGE_API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY', 'demo')
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY', 'demo')
    
    # Cache configuration
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 900  # 15 minutes
    
    # Scheduler configuration
    SCHEDULER_API_ENABLED = True

    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///wealth_vista.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
