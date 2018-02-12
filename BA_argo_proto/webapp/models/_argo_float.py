from . import db


class ArgoFloat(db.Model):
    __tablename__ = 'argo_floats'

    measurements = db.relationship('Measurement', backref='argo_floats', lazy='dynamic')

    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(10))
    project_name = db.Column(db.String(30))
    launch_date = db.Column(db.Date)
    float_owner = db.Column(db.String(60))

    def __init__(self, identifier, project_name, launch_date, float_owner):
        self.identifier = identifier
        self.project_name = project_name
        self.launch_date = launch_date
        self.float_owner = float_owner

    def __repr__(self):
        return f'<Argo Float {self.id!r}>'


class ArgoFloatTmpTable(ArgoFloat):
    __bind_key__ = 'data_input'
