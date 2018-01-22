from data import db_writer

for argo_float in db_writer:
    argo_float.write_data()
