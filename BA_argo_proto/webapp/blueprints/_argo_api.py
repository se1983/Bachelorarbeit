from flask import Blueprint, jsonify

from ..helpers import gen_last_seen, argo_data_table_as_dicts

argo_api = Blueprint('argo_api', __name__)


@argo_api.route("/last_seen")
@argo_api.route("/last_seen/<force_reload>")
def last_seen(force_reload=""):
    # TODO Read token from cfg
    # https://stackoverflow.com/questions/40730110/flask-using-host-parameter-with-blueprints-register-blueprint
    __token = '4e9fe9a5d862551cb67503ed630e1c80'

    argo_floats = gen_last_seen(force_reload=force_reload == __token)
    return jsonify(argo_floats)


@argo_api.route("/argo_float/<identifier>")
def get_argo_float(identifier):
    rows = argo_data_table_as_dicts(identifier)

    return jsonify({
        'pressure': [x['pressure'] for x in rows],
        'temperature': [x['temperature'] for x in rows],
        'salinity': [x['salinity'] for x in rows],
        'conductivity': [x['conductivity'] for x in rows],
        'timestamp': [x['timestamp'] for x in rows]
    })
