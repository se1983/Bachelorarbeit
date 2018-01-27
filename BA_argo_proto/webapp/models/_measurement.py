from . import db


class Measurement(db.Model):
    __tablename__ = 'measurements'

    id = db.Column(db.Integer, primary_key=True)

    profiles = db.relationship('Profile', backref='measurements', lazy='dynamic')

    argo_float_id = db.Column(db.Integer, db.ForeignKey('argo_floats.id'))
    argo_float = db.relationship('ArgoFloat')

    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    location = db.relationship('Location')

    def __init__(self, argo_float, location):
        self.argo_float = argo_float
        self.location = location

    def __repr__(self):
        return f'<Measurement {self.id!r}>'


class MeasurementTmpTable(Measurement):
    __bind_key__ = 'data_input'
