from webapp import db
from webapp.models import Measurement, Location, Profile, ArgoFloat

query = db.session.query(ArgoFloat, Location, Profile) \
                .join(Measurement) \
                .join(Location) \
                .join(Profile) \
                .filter(ArgoFloat.identifier == '1900037') \ 
                .order_by(Profile.timestamp)
            
result = db.session.execute(query, None, bind=db.get_engine(app, None))

data = [row for row in result]

