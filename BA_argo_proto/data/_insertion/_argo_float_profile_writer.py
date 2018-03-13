from webapp.models import ArgoFloat, Location, Measurement, Profile


class ArgoFloatProfile:
    def __init__(self, argo_float, db, app):
        """
        Writes the Profile of one ArgoFloat into the database.


        :param argo_float: Representation of the extracted Data of one ArgoFloat.
        :param db: ORM - Flask-SQLAlchemy
        :param app: Flask-app
        """

        self.argo_float = argo_float
        self.db = db
        self.app = app

    def write_data(self, bind=None):
        """
        Triggers the data-transfer.
        :param bind: str - Define a binding.
        """
        session = self.db.create_scoped_session(
            options={
                'bind': self.db.get_engine(self.app, bind),
                'binds': {}
            }
        )
        try:
            argo_float_ = ArgoFloat(
                identifier=self.argo_float.identifier,
                project_name=self.argo_float.project_name,
                launch_date=self.argo_float.launch_date,
                float_owner=self.argo_float.float_owner

            )
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
                    temperature=profile_data.temperature,
                    valid_data_range=profile_data.valid_data_ranges
                ))

            session.commit()
        except Exception as err:
            session.rollback()
            raise err
