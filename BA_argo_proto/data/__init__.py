from webapp import db, app
from ._extraction import ExtractorFactory
from ._insertion import DataBaseWriter


_data_folder = app.config['data_folder']
_data_sets = ExtractorFactory(_data_folder).get_data_sets()

float_count = ExtractorFactory(_data_folder).float_count()
db_writer = DataBaseWriter(argo_floats=_data_sets, db=db, app=app)

