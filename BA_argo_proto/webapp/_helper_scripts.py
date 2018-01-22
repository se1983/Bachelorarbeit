# @DOKU
import os.path
import pickle

extract_data = lambda t, r: [x['value'] for x in r if x['data_type'] == t]

from . import db, app


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


def argo_data_flat_datastructure(identifier, value=None):
    results = _sql_query('argo_data.sql', var=identifier)

    if value is None:
        return sorted([{
            # Extracting needed values from the SQL Alchemy result Object
            #
            # @DOC
            # - result is some weird and nasty thread-pool
            #   -> copying the values into a less complex Datastructure
            # - The Values have to be sorted by the time of the measurement.
            'location': (row['latitude'], row['longitude']),
            'timestamp': row['timestamp'],
            'measurement_id': row['measurement_id'],
            'data_type': row['data_type'],
            'value': row['value'],
            'profile_id': row['profile_id']
        } for row in results], key=lambda k: k['timestamp'])

    map_entries = {
        'location': lambda row: (row['latitude'], row['longitude']),
        'timestamp': lambda row: row['timestamp'],
        'measurement_id': lambda row: row['measurement_id'],
        'data_type': lambda row: row['data_type'],
        'value': lambda row: row['value'],
        'profile_id': lambda row: row['profile_id']
    }

    return sorted([map_entries[value].update(map_entries['timestamp']) for row in results],
                  key=lambda k: k['timestamp'])
    # @TODO Generic datastructure

