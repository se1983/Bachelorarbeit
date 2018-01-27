import urllib
from copy import deepcopy

from flask import url_for
from flask_script import Manager, Server, Shell, prompt_bool

from webapp import app, db
from data import db_writer

assert db is not None

# https://flask-script.readthedocs.io/en/latest/

manager = Manager(app)


@manager.command
def rebuild_db():

    print(f"Datafolder: {app.config['data_folder']}")
    if True or prompt_bool("Rebuild the database?"):

        session = db.create_scoped_session(
            options={
                'bind': db.get_engine(app, 'data_input'),
                'binds': {}
            }
        )

        db.drop_all(bind=['data_input'], app=app)
        db.create_all(bind=['data_input'], app=app)

        for argo_float in db_writer:
            argo_float.write_data(bind='data_input')


@manager.command
def list_routes():
    """
    comes frome here: http://flask.pocoo.org/snippets/117/
    :return:
    """
    output = []
    for rule in app.url_map.iter_rules():
        options = {arg: f"[{arg}]" for arg in rule.arguments}

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)


manager.add_command("runserver", Server())
manager.add_command("shell", Shell())

if __name__ == "__main__":
    manager.run()
