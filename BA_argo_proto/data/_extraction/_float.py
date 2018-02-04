import os

import numpy as np

from ._data_set import FloatDataset
from ._data_set_context_manager import DatasetContextManager

class Float(object):
    def __init__(self, datafolder_path):
        self.identifier = datafolder_path.split("/")[-1]
        self.data = self.__extract_float_data(self.__data_files(datafolder_path + '/profiles/'))

    def get_last_position(self):
        pos = self.data[-1].position \
            if len(self.data[-1].position) >= 1 else {'latitude': np.nan, 'longitude': np.nan}
        return pos.update({'Float': self.identifier})

    @staticmethod
    def __data_files(profiles_path):
        return \
            (os.path.join(path, name) for path, subdirs, files in os.walk(profiles_path) for name in files)

    @staticmethod
    def __extract_float_data(file_paths):
        return \
            (FloatDataset(p) for p in file_paths)

    def __extract_meta_data(self, file_path):
        with DatasetContextManager(file_path) as ds:
            pass


    def __repr__(self):
        return \
            f"""This is Argo Float {self.identifier}."""
