from numpy import nan


def positions_json(rows, identifier):
    """
    GeoJSON for the position-history of one argofloat.

    :param rows: dict - representation of database request
    :param identifier: str - identifier of the argofloat
    :return: [{k,v}] - nested structure for the geoJSON
    """
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
    """
    JSON for the measurement-data.

    :param rows: dict - representation of database request
    :return: [{k,v}] - nested structure for the JSON
    """
    time_string = '%d. %B %Y'

    data = {
        'pressure': [x['pressure'] for x in rows['measurements']],
        'temperature': [x['temperature'] for x in rows['measurements']],
        'salinity': [x['salinity'] for x in rows['measurements']],
        'timestamp': [x['timestamp'] for x in rows['measurements']],
        'valid': all([x['valid_data'] for x in rows['measurements']]),
        'float_owner': rows['float_owner'],
        'project_name': rows['project_name'],
        'launch_date': rows['launch_date'].strftime(time_string),
        'last_seen': rows['measurements'][-1]['timestamp'].strftime(time_string),
        'identifier': rows['identifier']
    }

    return data


def last_seen_json(rows):
    """
    GeoJSON for the featurecollection of last seen.

    :param rows: dict - representation of database request
    :return: [{k,v}] - nested structure for the geoJSON
    """
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
