from ._argo_float_profile_writer import ArgoFloatProfile


class DataBaseWriter:
    def __init__(self, argo_floats, db, app):
        """
        Interface to write the data as sequence.

        :param argo_floats: generator - Graph of the representation of the Data.
        :param db: ORM - Flask-SQLAlchemy
        :param app: Flask-app
        """
        self.argo_floats = argo_floats
        self.db = db
        self.app = app

    def __iter__(self):
        return self

    def __next__(self):
        """
        Follow the sequence.

        :return: ArgoFloatProfile
        """
        self.argo_float = next(self.argo_floats)
        return ArgoFloatProfile(self.argo_float, self.db, self.app)
