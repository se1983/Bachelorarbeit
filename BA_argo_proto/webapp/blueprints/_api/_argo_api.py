import os

import pickle
from flask import Blueprint, jsonify

from webapp import app

from . import _queries as queries

from ._json_builder import positions_json, argo_float_data_json, last_seen_json

argo_api = Blueprint('argo_api', __name__)


@argo_api.route("/last_seen")
@argo_api.route("/last_seen/<force_reload>")
def last_seen(force_reload=""):
    """Route for the latest position of the argofloats.

    :returns {json-request}
    """
    __token = app.config['FORCE_RELOAD_TOKEN']
    __cache_file_path = f'{app.root_path}/last_seen.pickle'

    if force_reload == __token or not os.path.isfile(__cache_file_path):
        argo_floats = last_seen_json(queries.last_seen())
        pickle.dump(argo_floats, open(__cache_file_path, 'wb'))
    else:
        argo_floats = pickle.load(open(__cache_file_path, 'rb'))

    return jsonify(argo_floats)


@argo_api.route("/argo_float/<identifier>")
def get_argo_float(identifier):
    """Route for the data of one argofloat.

    :returns {json-request}
    """
    rows = queries.argo_data(identifier)

    return jsonify(argo_float_data_json(rows))


@argo_api.route("/positions/<identifier>")
def get_argo_float_position_history(identifier):
    """Route for the position history of one argofloat.

    :returns {json-request}
    """
    rows = queries.argo_positions(identifier)

    geo_json = {
        "type": "FeatureCollection",
        "features": positions_json(rows, identifier)
    }
    return jsonify(geo_json)
