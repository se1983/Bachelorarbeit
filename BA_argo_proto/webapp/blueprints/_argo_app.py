from flask import Blueprint, render_template

argo_app = Blueprint('argo_app', __name__, template_folder='templates')


@argo_app.route("/")
def index():
    return render_template('map.html')


@argo_app.route("/test")
def test_pattern():
    return render_template('test_pattern.html')
