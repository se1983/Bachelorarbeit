from flask import Blueprint, jsonify

from . import gen_last_seen, argo_data_flat_datastructure, extract_data

argo_api = Blueprint('argo_api', __name__)


@argo_api.route("/last_seen")
@argo_api.route("/last_seen/<force_reload>")
def last_seen(force_reload=""):

    __token = '4e9fe9a5d862551cb67503ed630e1c80'

    argo_floats = gen_last_seen(force_reload=force_reload == __token)
    return jsonify(argo_floats)


@argo_api.route("/argo_float/<identifier>")
def get_argo_float(identifier):
    rows = argo_data_flat_datastructure(identifier)

    return jsonify({
        'pressure': extract_data('pressure', rows),
        'temperature': extract_data('temperature', rows),
        'salinity': extract_data('salinity', rows),
        'conductivity': extract_data('conductivity', rows),
        'location': [x['location'] for x in rows],
        'timestamp': [x['timestamp'] for x in rows]
    })


@argo_api.route("/argo_float/<identifier>/<data>")
def get_data_from_float(identifier, data):
    rows = argo_data_flat_datastructure(identifier)

    return jsonify([{
        'value': x,
        'date': rows[i]['timestamp']
    } for i, x in enumerate(extract_data(data, rows))])
