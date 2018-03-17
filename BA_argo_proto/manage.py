import urllib

from tqdm import tqdm
from flask import url_for
from flask_script import Manager, Server, Shell, prompt_bool

from webapp import app, db
from data import ExtractorFactory, DataBaseWriter

assert db is not None

manager = Manager(app)


@manager.command
def rebuild_db():
    """Rebuilds the temporarily Database from local netCDF-Data"""

    argo_data_dir = app.config['ARGO_DATA_DIRECTORY']

    print(f"Datafolder: {argo_data_dir}")

    _extractor = ExtractorFactory(argo_data_dir)
    float_count = _extractor.float_count()

    db_writer = DataBaseWriter(
        argo_floats=_extractor.get_data_sets(), db=db, app=app
    )

    print(float_count)

    if app.config['ARGO_AUTO_REBUILD'] or prompt_bool("Rebuild the database?"):
        db.drop_all(bind=['data_input'], app=app)
        db.create_all(bind=['data_input'], app=app)

        for argo_float in tqdm(db_writer, total=float_count):
            argo_float.write_data(bind='data_input')


@manager.command
def list_routes():
    """
    Lists all routes of the Flask Application
    """

    def generate_route_string(rule):
        options = {arg: f"[{arg}]" for arg in rule.arguments}

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        return urllib.parse.unquote(f"{rule.endpoint:50s} {methods:20s} {url}")

    for line in [generate_route_string(rule) for rule in app.url_map.iter_rules()]:
        print(line)


manager.add_command("runserver", Server(threaded=True, host="127.0.0.1", port=9000))
manager.add_command("shell", Shell())

if __name__ == "__main__":
    manager.run()
