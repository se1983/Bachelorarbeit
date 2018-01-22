from webapp import db, app
from ._extraction import data_extractor
from ._insertion import database_writer


_data_folder = app.config['data_folder']
_data_sets = data_extractor.ExtractorFactory(_data_folder).get_data_sets()
db_writer = database_writer.DataBaseWriter(argo_floats=_data_sets, db=db)
