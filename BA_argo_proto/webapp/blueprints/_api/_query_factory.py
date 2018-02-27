from flask_sqlalchemy import BaseQuery

from webapp import db, app
from webapp.models import Measurement, Location, Profile, ArgoFloat


class QueryFactory(object):

    def __init__(self):
        pass

    @staticmethod
    def __execute(query, bind=None):

        return {
            BaseQuery: lambda q: db.session.execute(q, None, bind=db.get_engine(app, bind)),
            str: lambda q: db.engine.execute(q)
        }[type(query)](query)

    @staticmethod
    def __load_template(file_name):
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

            result_proxy = self.__execute(query)
            keys = result_proxy.keys()

            measurements = [
                {
                    'timestamp': row[keys.index('profiles_timestamp')],
                    'temperature': row[keys.index('profiles_temperature')],
                    'salinity': row[keys.index('profiles_salinity')],
                    'pressure': row[keys.index('profiles_pressure')],
                    'valid_data': row[keys.index('profiles_valid_data_range')]
                } for row in result_proxy
            ]

            query = db.session.query(ArgoFloat) \
                .filter(ArgoFloat.identifier == identifier)
            result_proxy = self.__execute(query)

            row = result_proxy.fetchone()
            keys = result_proxy.keys()
            print(row)

            data = {
                'measurements': measurements,
                'float_owner': row[keys.index('argo_floats_float_owner')],
                'project_name': row[keys.index('argo_floats_project_name')],
                'launch_date': row[keys.index('argo_floats_launch_date')],
                'identifier': identifier
            }

            return data
        except Exception as err:
            print(err)
            db.session.rollback()

    def last_seen(self):
        return self.__execute(self.__load_template('last_seen.sql'))

    def argo_positions(self, identifier):
        try:
            query = db.session.query(ArgoFloat, Location, Profile) \
                .join(Measurement) \
                .join(Location) \
                .join(Profile) \
                .filter(ArgoFloat.identifier == identifier) \
                .order_by(Profile.timestamp)

            result_proxy = self.__execute(query)
            keys = result_proxy.keys()

            data = [{
                'location': (row[keys.index('locations_longitude')],
                             row[keys.index('locations_latitude')]),
                'timestamp': row[keys.index('profiles_timestamp')],
                'temperature': row[keys.index('profiles_temperature')],
                'salinity': row[keys.index('profiles_salinity')],
                'pressure': row[keys.index('profiles_pressure')]
            } for row in result_proxy]

            return data
        except Exception as err:
            print(err)
            db.session.rollback()
