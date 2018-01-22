from netCDF4 import Dataset

class DatasetContextManager(object):
    def __init__(self, file_path):
        self.ds = Dataset(file_path)

    def __enter__(self):
        return self.ds

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ds.close() 
