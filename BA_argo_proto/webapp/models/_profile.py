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
    conductivity = db.Column(db.Float)
    temperature = db.Column(db.Float)

    def __init__(self, cycle, timestamp, measurement, salinity, pressure, conductivity, temperature):
        self.cycle = cycle
        self.timestamp = timestamp
        self.measurement = measurement

        self.salinity = float(salinity)
        self.pressure = float(pressure)
        self.conductivity = float(conductivity)
        self.temperature = float(temperature)


    def __repr__(self):
        return f'<Profile {self.id!r}>'


class ProfileTmpTable(Profile):
    __bind_key__ = 'data_input'
