from . import db


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    cycle = db.Column(db.Integer)
    timestamp = db.Column(db.Date)

    records = db.relationship('Record', backref='profiles', lazy='dynamic')

    measurement_id = db.Column(db.Integer, db.ForeignKey('measurements.id'))
    measurement = db.relationship('Measurement')

    def __init__(self, cycle, timestamp, measurement):
        self.cycle = cycle
        self.timestamp = timestamp
        self.measurement = measurement

    def __repr__(self):
        return f'<Profile {self.id!r}>'


class ProfileTmpTable(Profile):
    __bind_key__ = 'data_input'
