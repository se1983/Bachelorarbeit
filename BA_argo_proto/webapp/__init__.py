from flask import Flask, url_for
from flask_twisted import Twisted

from .models import db

app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('./argo.cfg')

db.init_app(app)

from .blueprints import argo_api, argo_app

app.register_blueprint(argo_api)
app.register_blueprint(argo_app)

from . import models

twisted = Twisted(app)
