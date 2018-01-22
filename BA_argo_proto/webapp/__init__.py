from flask import Flask

from .models import db

# http://flask.pocoo.org/docs/0.12/patterns/appfactories/

app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('./argo.cfg')
app.config['data_folder'] = "/root/201708-ArgoData/aoml/"

db.init_app(app)

from .blueprints import argo_api, argo_app

app.register_blueprint(argo_api)
app.register_blueprint(argo_app)

# Announce all routes of the Application

from . import models
