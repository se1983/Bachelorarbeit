import os

import pickle
from flask import Blueprint, jsonify

from webapp import app

from . import _queries as queries

from ._geojson_builder import positions_geojson, argo_float_data, last_seen

argo_api = Blueprint('argo_api', __name__)


@argo_api.route("/last_seen")
@argo_api.route("/last_seen/<force_reload>")
def last_seen(force_reload=""):
    __token = app.config['FORCE_RELOAD_TOKEN']
    __cache_file_path = f'{app.root_path}/last_seen.pickle'

    if force_reload == __token or not os.path.isfile(__cache_file_path):
        argo_floats = last_seen(queries.last_seen())
        pickle.dump(argo_floats, open(__cache_file_path, 'wb'))
    else:
        argo_floats = pickle.load(open(__cache_file_path, 'rb'))

    return jsonify(argo_floats)


@argo_api.route("/argo_float/<identifier>")
def get_argo_float(identifier):
    rows = queries.argo_data(identifier)

    return jsonify(argo_float_data(rows))


@argo_api.route("/positions/<identifier>")
def get_argo_float_position_history(identifier):
    rows = queries.argo_positions(identifier)

    geo_json = {
        "type": "FeatureCollection",
        "features": positions_geojson(rows, identifier)
    }
    return jsonify(geo_json)
