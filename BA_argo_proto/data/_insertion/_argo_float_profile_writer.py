from webapp.models import ArgoFloat, Location, Measurement, Profile, Record


# TODO: Think about: To write the ArgoFloatProfile into the database we have dependencies to webapp.models.
# Is there a better way, following the dependency inversion principle to inject the handler for writing a
# Argo-Float Profile?
# If this is the wrong position for this class, then where to put it? It is either a model neither something
#  used by the webapp.

class ArgoFloatProfile:
    def __init__(self, argo_float, db, app):
        self.argo_float = argo_float

        self.db = db
        self.app = app

    def write_data(self, bind=None):

        session = self.db.create_scoped_session(
            options={
                'bind': self.db.get_engine(self.app, bind),
                'binds': {}
            }
        )

        # http://flask.pocoo.org/docs/0.12/appcontext/
        argo_model = ArgoFloat(identifier=self.argo_float.identifier)

        for __data_set in self.argo_float.data:
            # This is the block i don't like:
            location_model = Location(latitude=__data_set.position['latitude'],
                                      longitude=__data_set.position['longitude'])
            measurement_model = Measurement(argo_float=argo_model,
                                            location=location_model)

            records = (
                Record(data_type='pressure', value=__data_set.pressure),
                Record(data_type='temperature', value=__data_set.temperature),
                Record(data_type='salinity', value=__data_set.salinity),
                Record(data_type='conductivity', value=__data_set.conductivity)
            )

            profile = Profile(cycle=int(__data_set.cycle_number),
                              timestamp=__data_set.date_creation,
                              measurement=measurement_model,
                              records=records)

            session.add(profile)

        session.commit()
