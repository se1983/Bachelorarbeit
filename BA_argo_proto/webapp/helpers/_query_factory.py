from sqlalchemy.dialects import postgresql

from webapp import db, app
from webapp.models import Measurement, Location, Profile, ArgoFloat


class QueryFactory(object):

    def __init__(self):
        pass

    @staticmethod
    def __execute(raw_sql):
        return db.engine.execute(raw_sql)

    def __load_template(self, file_name):
        with open(f'{app.root_path}/{app.template_folder}/{file_name}') as raw_sql:
            sql = raw_sql.read()
        return sql

    def argo_data(self, identifier):

        try:
            query = db.session.query(ArgoFloat, Profile) \
                .join(Measurement) \
                .join(Location) \
                .join(Profile) \
                .filter(ArgoFloat.identifier == identifier) \
                .order_by(Profile.timestamp)

            return [
                {
                    'timestamp': elem[1].timestamp,
                    'temperature': elem[1].temperature,
                    'salinity': elem[1].salinity,
                    'conductivity': elem[1].conductivity
                } for elem in query.yield_per(200)
            ]

        except Exception as err:
            print(err)
            db.session.rollback()
