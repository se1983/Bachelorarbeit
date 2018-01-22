engine = create_engine('sqlite:///argo.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

r1 = Record(data_type="Temperature", value=15, profile=Profile(datetime.now()))

p1 = Profile(timestamp=datetime.now() - timedelta(days=3))
p1.records = [Record(data_type="Temperature", value=25),
              Record(data_type="Pressure", value=55)]

try:
    session.add(r1)
    session.add(p1)
    session.commit()
except Exception as err:
    print(err)
    session.rollback()
