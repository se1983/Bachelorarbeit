from ._argo_float_profile_writer import ArgoFloatProfile


class DataBaseWriter:
    def __init__(self, argo_floats, db, app):
        self.argo_floats = argo_floats
        self.db = db
        self.app = app

    def __iter__(self):
        return self

    def __next__(self):
        self.argo_float = next(self.argo_floats)
        return ArgoFloatProfile(self.argo_float, self.db, self.app)
