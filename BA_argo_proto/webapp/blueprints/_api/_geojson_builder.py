from numpy import nan


def positions_json(rows, identifier):
    # Nan is not part of parsable JSON so wer will convert this value to None(Null)
    __extract = lambda f: f"{f:.2f}" if not f is nan else ''

    transfer_points = [
        {
            "type": "Feature",
            "properties": {
                # The first element is of type position_history_start
                # every other element is of type postion_history.
                'feature_type': 'position_history_start' if i <= 0 else 'position_history',
                'name': 'EPSG:4326',
                'timestamp': feature['timestamp'],
                'temperature': __extract(feature['temperature']),
                'salinity': __extract(feature['salinity']),
                'pressure': __extract(feature['pressure']),
                'transfer_number': i,
                'identifier': identifier
            },
            "geometry": {
                "type": "Point",
                "coordinates": [*feature['location']]
            }
        }
        for i, feature in enumerate(rows)]

    __nodes = [point['location'] for point in rows]

    edge_features = [
        {
            "type": "Feature",
            "properties": {
                # The first element is of type position_history_start
                # every other element is of type postion_history.
                'feature_type': 'position_history_edge',
                'name': 'EPSG:4326',
                'identifier': identifier
            },
            "geometry": {
                "type": "LineString",
                "coordinates": __nodes
            }
        }
    ]

    return transfer_points + edge_features


def argo_float_data_json(rows):
    return {
        'pressure': [x['pressure'] for x in rows],
        'temperature': [x['temperature'] for x in rows],
        'salinity': [x['salinity'] for x in rows],
        'conductivity': [x['conductivity'] for x in rows],
        'timestamp': [x['timestamp'] for x in rows]
    }


def last_seen_json(rows):
    return {'type': "FeatureCollection",
            'crs': {
                'type': 'name',
                'properties': {
                    'name': 'EPSG:4326'
                }
            }, 'features': [{"type": "Feature",
                             "geometry": {"type": "Point",
                                          "coordinates": [lon, lat]},
                             "properties": {
                                 'feature_type': 'latest_position',
                                 "identifier": argo_float,
                                 "last_seen": last_seen
                             }
                             } for (argo_float, lon, lat, last_seen) in rows]
            }
