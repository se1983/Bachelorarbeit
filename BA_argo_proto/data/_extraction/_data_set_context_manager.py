from netCDF4 import Dataset


class DatasetContextManager(object):
    def __init__(self, file_path):
        """
        Contextmanager to open a netCDF-File

        :param file_path: path to the file.
        """

        self.ds = Dataset(file_path)

    def __enter__(self):
        return self.ds

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the dataset."""
        self.ds.close()
