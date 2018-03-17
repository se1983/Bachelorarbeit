from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from ._measurement import Measurement
from ._argo_float import ArgoFloat
from ._location import Location
from ._profile import Profile
