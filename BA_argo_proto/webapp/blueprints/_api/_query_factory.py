from flask_sqlalchemy import BaseQuery

from webapp import db, app
from webapp.models import Measurement, Location, Profile, ArgoFloat


class QueryFactory(object):

    @staticmethod
    def __execute(query, bind=None):
        """
        Executing a query.


        :param query: SQLAlchemy.BaseQuery or str  - Can be a raw string or a query object.
        :param bind: str - Define a binding.
        :return: SQLAlchemy.result_proxy - Result of the execution.
        """
        return {
            BaseQuery: lambda q: db.session.execute(q, None, bind=db.get_engine(app, bind)),
            str: lambda q: db.engine.execute(q)
        }[type(query)](query)

    @staticmethod
    def __load_template(file_name):
        """
        Loading raw SQL Statement from file.

        :param file_name: str - Path to the file
        :return: str - SQL-Code
        """
        with open(f'{app.root_path}/{app.template_folder}/{file_name}') as raw_sql:
            sql = raw_sql.read()
        return sql

    def argo_data(self, identifier):
        """
        Extract the measurement data of one ArgoFloat.

        :param identifier: str - Identifier of the ArgoFloat
        :return: dict - Executed table representation of the result.
        """
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
        """
        Extract the latest positions of all ArgoFloats.

        :return: dict - Executed table representation of the result.
        """
        return self.__execute(self.__load_template('last_seen.sql'))

    def argo_positions(self, identifier):
        """
        Extract the position history of one ArgoFloat.

        :param identifier: str - Identifier of the ArgoFloat
        :return: dict - Executed table representation of the result.
        """
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
