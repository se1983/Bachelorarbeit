import os

import pickle
from flask import Blueprint, jsonify

from webapp import app
from ..helpers import queries

argo_api = Blueprint('argo_api', __name__)


@argo_api.route("/last_seen")
@argo_api.route("/last_seen/<force_reload>")
def last_seen(force_reload=""):
    # TODO Read token from cfg
    # https://stackoverflow.com/questions/40730110/flask-using-host-parameter-with-blueprints-register-blueprint
    __token = '4e9fe9a5d862551cb67503ed630e1c80'
    __cache_file_path = f'{app.root_path}/last_seen.pickle'

    if force_reload == __token or not os.path.isfile(__cache_file_path):
        results = queries.last_seen()
        argo_floats = {'type': "FeatureCollection",
                       'crs': {
                           'type': 'name',
                           'properties': {
                               'name': 'EPSG:4326'
                           }
                       }, 'features': results}
        pickle.dump(argo_floats, open(__cache_file_path, 'wb'))
    else:
        argo_floats = pickle.load(open(__cache_file_path, 'rb'))

    return jsonify(argo_floats)


@argo_api.route("/argo_float/<identifier>")
def get_argo_float(identifier):
    rows = queries.argo_data(identifier)

    return jsonify({
        'pressure': [x['pressure'] for x in rows],
        'temperature': [x['temperature'] for x in rows],
        'salinity': [x['salinity'] for x in rows],
        'conductivity': [x['conductivity'] for x in rows],
        'timestamp': [x['timestamp'] for x in rows]
    })


@argo_api.route("/positions/<identifier>")
def get_argo_float_position_history(identifier):
    rows = queries.argo_positions(identifier)

    transfer_points = [
        {
            "type": "Feature",
            "properties": {
                # The first element is of type position_history_start
                # every other element is of type postion_history.
                'feature_type': 'position_history_start' if i <= 0 else 'position_history',
                'name': 'EPSG:4326',
                'timestamp': feature['timestamp'],
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

    geo_json = {
        "type": "FeatureCollection",
        "features": transfer_points + edge_features
    }
    return jsonify(geo_json)
