import os
import logging
from flask import Flask
from flask_caching import Cache
from werkzeug.middleware.proxy_fix import ProxyFix
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
import pytz

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure cache
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 900  # 15 minutes
cache = Cache(app)

# Configure timezone
IST = pytz.timezone('Asia/Kolkata')

# Import and initialize database
from config import Config
app.config.from_object(Config)

from db import init_db
init_db(app)

# Import routes
from routes.main import main_bp
from routes.api import api_bp

app.register_blueprint(main_bp)
app.register_blueprint(api_bp, url_prefix='/api')

# Make cache available to api routes
import routes.api
routes.api.cache = cache

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Import and start background data fetching
from services.scheduler import start_data_fetching
start_data_fetching(scheduler, cache)

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
