from webapp.models import ArgoFloat, Location, Measurement, Profile, Record


# TODO: Think about: To write the ArgoFloatProfile into the database we have dependencies to webapp.models.
# Is there a better way, following the dependency inversion principle to inject the handler for writing a
# Argo-Float Profile?
# If this is the wrong position for this class, then where to put it? It is either a model neither something
#  used by the webapp.

class ArgoFloatProfile:
    def __init__(self, argo_float, db):
        self.argo_float = argo_float

        self.db = db

    def write_data(self):
        print(f"Writing Argo Float {self.argo_float.identifier} to database.")

        # http://flask.pocoo.org/docs/0.12/appcontext/
        argo_model = ArgoFloat(identifier=self.argo_float.identifier)
        #self.db.session.add(argo_model)

        for ds in self.argo_float.data:
            location_model = Location(latitude=ds.position['latitude'], longitude=ds.position['longitude'])

            measurement_model = Measurement(argo_float=argo_model, location=location_model)
            profile_model = Profile(cycle=int(ds.cycle_number), timestamp=ds.date_creation,
                                    measurement=measurement_model)
            pressure_record_model = Record(data_type='pressure', value=ds.pressure, profile=profile_model)
            temperature_record_model = Record(data_type='temperature', value=ds.temperature, profile=profile_model)
            salinity_record_model = Record(data_type='salinity', value=ds.salinity, profile=profile_model)
            conductivity_record_model = Record(data_type='conductivity', value=ds.conductivity,
                                               profile=profile_model)

            #[self.db.session.add(x) for x in (profile_model,
            #                                  location_model,
            #                                  measurement_model,
            #                                  pressure_record_model,
            #                                  temperature_record_model,
            #                                  salinity_record_model,
            #                                  conductivity_record_model)]
        self.db.session.add(argo_model)
        self.db.session.commit()
