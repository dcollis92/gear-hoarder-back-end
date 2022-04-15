from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from api.models.db import db
from config import Config

# ============ Import Models ============
from api.models.user import User
from api.models.profile import Profile
from api.models.rig import Rig
from api.models.guitar import Guitar
from api.models.amp import Amp
from api.models.pedal import Pedal
from api.models.association import Association

# ============ Import Views ============
from api.views.auth import auth
from api.views.rigs import rigs
from api.views.guitars import guitars
from api.views.amps import amps
from api.views.pedals import pedals


cors = CORS()
migrate = Migrate() 
list = ['GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE', 'LINK']

def create_app(config):
  app = Flask(__name__)
  app.config.from_object(config)

  db.init_app(app)
  migrate.init_app(app, db)
  cors.init_app(app, supports_credentials=True, methods=list)

  # ============ Register Blueprints ============
  app.register_blueprint(auth, url_prefix='/api/auth') 
  app.register_blueprint(rigs, url_prefix='/api/rigs')
  app.register_blueprint(guitars, url_prefix='/api/guitars')
  app.register_blueprint(amps, url_prefix='/api/amps')
  app.register_blueprint(pedals, url_prefix='/api/pedals')

  return app

app = create_app(Config)