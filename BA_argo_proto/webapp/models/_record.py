from . import db


class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    data_type = db.Column(db.String(30))
    value = db.Column(db.Float)

    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    profile = db.relationship('Profile')

    def __init__(self, data_type, value, profile):
        self.value = float(value)
        self.data_type = data_type

        self.profile = profile

    def __repr__(self):
        return f'<Record {self.id!r}>'


class RecordTmpTable(Record):
    __bind_key__ = 'data_input'
