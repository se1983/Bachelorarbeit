from . import db


class ArgoFloat(db.Model):
    __tablename__ = 'argo_floats'

    measurements = db.relationship('Measurement', backref='argo_floats', lazy='dynamic')

    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(10))

    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return f'<Argo Float {self.id!r}>'


class ArgoFloatTmpTable(ArgoFloat):
    __bind_key__ = 'data_input'
