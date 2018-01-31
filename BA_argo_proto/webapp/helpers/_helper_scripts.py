# @DOKU
import os.path
import pickle

from numpy import nan

from webapp import db, app


def _sql_query(file_name, var=None):
    with open(f'{app.root_path}/{app.template_folder}/{file_name}') as raw_sql:
        sql = raw_sql.read()

    return db.engine.execute(sql if var is None else sql % var)


def _feature_list(rows):
    return [{"type": "Feature",
             "geometry": {"type": "Point",
                          "coordinates": [lon, lat]},
             "properties": {"Argo Float": argo_float,
                            "last seen": last_seen}
             } for (argo_float, lon, lat, last_seen) in rows]


def gen_last_seen(force_reload=False):
    cache_file = f'{app.root_path}/.last_seen.pickle'

    if not os.path.isfile(cache_file) or force_reload:
        results = _sql_query('last_seen.sql')

        data = {'type': "FeatureCollection",
                'crs': {
                    'type': 'name',
                    'properties': {
                        # Projectiontype @TODO Documentation projection types in openlayers
                        'name': 'EPSG:4326'
                    }
                }, 'features': _feature_list(results)}

        pickle.dump(data, open(cache_file, 'wb'))
    else:
        data = pickle.load(open(cache_file, 'rb'))

    return data


def argo_data_table_as_dicts(identifier):
    """
    Get the data of one specific ArgoFloat as dictionary.

    :param identifier: Argo Float identifier.
    :return: list(dicts): Data of ArgoFloat<identifier>.
    """
    results = _sql_query('argo_data.sql', var=identifier)

    return sorted([{
        'location': (row['latitude'], row['longitude']),
        'timestamp': row['timestamp'],
        'measurement_id': row['measurement_id'],
        'pressure': row['pressure'],
        'salinity': row['salinity'],
        'conductivity': row['conductivity'],
        'temperature': row['temperature'],
        } for row in results], key=lambda k: k['timestamp'])
