from webapp.models import ArgoFloat, Location, Measurement, Profile


class ArgoFloatProfile:
    def __init__(self, argo_float, db, app):
        """
        This writes the extracted data of an Argo Float into the database.

        :param argo_float: ArgoFloat Datahandler (_extraction._float.Float)
        :param db: SQLAlchemy
        :param app: Flask App
        """
        self.argo_float = argo_float
        self.db = db
        self.app = app

    def write_data(self, bind=None):
        """
        Writing the Data of this ArgoFloat into the database.

        :param bind: SQLAlchemy bind (optional).
        """

        # Create a session into the SQLAlchemy bind.  (see argo.cfg)
        # Scoped-session: http://flask-sqlalchemy-session.readthedocs.io/en/v1.1/
        # TODO: sessionfactory
        session = self.db.create_scoped_session(
            options={
                'bind': self.db.get_engine(self.app, bind),
                'binds': {}
            }
        )

        try:
            argo_float_ = ArgoFloat(identifier=self.argo_float.identifier)
            # Collecting the Data of each Profile of the ArgoFloat
            for profile_data in self.argo_float.data:
                location_ = Location(
                    latitude=profile_data.position['latitude'],
                    longitude=profile_data.position['longitude']
                )
                measurement_ = Measurement(
                    argo_float=argo_float_,
                    location=location_
                )

                session.add(Profile(
                    cycle=int(profile_data.cycle_number),
                    timestamp=profile_data.date_creation,
                    measurement=measurement_,
                    salinity=profile_data.salinity,
                    pressure=profile_data.pressure,
                    conductivity=profile_data.conductivity,
                    temperature=profile_data.temperature
                ))

            session.commit()
        except Exception as err:
            # Something went wrong. Rollback all changes before raising the exception again.
            # The Data should always written as once. So there will be no mercy at this point.
            session.rollback()
            raise err
