import datetime
import os

import numpy as np

from ._data_set import FloatDataset
from ._data_set_context_manager import DatasetContextManager
from ._extract_dataset import extract_variable, string_from_bytearray


class Float(object):
    def __init__(self, datafolder_path):
        self.identifier = datafolder_path.split("/")[-1]
        self.project_name = None
        self.launch_date = None
        self.float_owner = None

        self.data = self.__extract_float_data(self.__data_files(datafolder_path + '/profiles/'))
        self.__extract_meta_data(self.__meta_file(datafolder_path))

    def get_last_position(self):
        pos = self.data[-1].position \
            if len(self.data[-1].position) >= 1 else {'latitude': np.nan, 'longitude': np.nan}
        return pos.update({'Float': self.identifier})

    @staticmethod
    def __data_files(profiles_path):
        return \
            (os.path.join(path, name) for path, subdirs, files in os.walk(profiles_path) for name in files)

    @staticmethod
    def __meta_file(base_path):
        return \
            os.path.join(
                base_path, [file for file in os.listdir(base_path) if file.endswith('_meta.nc')][0]
            )


    @staticmethod
    def __extract_float_data(file_paths):
        return \
            (FloatDataset(p) for p in file_paths
             # Don use the control and metafiles.
             if not any([pattern in p for pattern in ('_prof', '_meta', '_tech', '_Rtraj')]))

    def __extract_meta_data(self, file_path):

        with DatasetContextManager(file_path) as ds:
            self.project_name = string_from_bytearray(extract_variable(ds, 'PROJECT_NAME'))
            self.launch_date = datetime.datetime.strptime(
                string_from_bytearray(extract_variable(ds, 'LAUNCH_DATE')),
                '%Y%m%d%H%M%S'
            )
            self.float_owner = string_from_bytearray(extract_variable(ds, 'FLOAT_OWNER'))

    def __repr__(self):
        return \
            f"""This is Argo Float {self.identifier}."""
