 
class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    timestamp = Column(Date)

    def __init__(self, timestamp):
        self.timestamp = timestamp

    def __repr__(self):
        return f'<Profile {self.id!r}>'
