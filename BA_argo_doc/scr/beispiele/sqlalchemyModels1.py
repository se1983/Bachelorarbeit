 
class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    data_type = Column(String(30))
    value = Column(Float)

    profile_id = Column(Integer, ForeignKey('profiles.id'))
    profile = relation('Profile', backref='records', lazy=False)

    def __init__(self, data_type, value, profile=None):
        self.value = float(value)
        self.data_type = data_type

        self.profile = profile

    def __repr__(self):
        return f'<Record {self.id!r}>'
