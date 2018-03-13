from . import db


class Location(db.Model):
    """Representation of one Location."""

    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    measurements = db.relationship('Measurement', backref='locations', lazy='dynamic')

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f'<Location {self.id!r}>'


class LocationTmpTable(Location):
    __bind_key__ = 'data_input'
