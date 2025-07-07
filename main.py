from flask import Flask
from flask_caching import Cache
from routes import main_bp
from routes.api import api_bp
from apscheduler.schedulers.background import BackgroundScheduler
from services.scheduler import start_data_fetching
import logging

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Register Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(api_bp, url_prefix='/api')

# Inject cache into api routes manually
import routes.api
routes.api.cache = cache

# ✅ Fix scheduler usage
scheduler = BackgroundScheduler()
scheduler.start()
start_data_fetching(scheduler, cache)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
print(app.url_map)
