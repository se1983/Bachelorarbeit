from . import db


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    cycle = db.Column(db.Integer)
    timestamp = db.Column(db.Date)

    measurement_id = db.Column(db.Integer, db.ForeignKey('measurements.id'))
    measurement = db.relationship('Measurement')

    salinity = db.Column(db.Float)
    pressure = db.Column(db.Float)
    temperature = db.Column(db.Float)
    valid_data_range = db.Column(db.Boolean)

    def __init__(self, cycle, timestamp, measurement, salinity, pressure, temperature, valid_data_range):
        self.cycle = cycle
        self.timestamp = timestamp
        self.measurement = measurement

        self.salinity = float(salinity)
        self.pressure = float(pressure)
        self.temperature = float(temperature)

        self.valid_data_range = bool(valid_data_range)

    def __repr__(self):
        return f'<Profile {self.id!r}>'


class ProfileTmpTable(Profile):
    __bind_key__ = 'data_input'
