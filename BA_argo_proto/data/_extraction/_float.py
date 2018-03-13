import datetime
import os

from ._data_set import FloatDataset
from ._data_set_context_manager import DatasetContextManager
from ._extract_dataset import extract_variable, string_from_bytearray


class Float(object):
    def __init__(self, datafolder_path):
        """
        Extractor-representation of one ArgoFloat.

            Reads netCDF

        :param datafolder_path: Path to the datafolder.
        """
        self.identifier = datafolder_path.split("/")[-1]
        self.project_name = None
        self.launch_date = None
        self.float_owner = None

        self.data = self.__extract_float_data(self.__data_files(datafolder_path + '/profiles/'))
        self.__extract_meta_data(self.__meta_file(datafolder_path))

    @staticmethod
    def __data_files(profiles_path):
        """
        Extracts the datafiles.

        :param profiles_path: Path to the profiles-directory of the current ArgoFloat.
        :return: Generator  - Full paths of all files in the directory.
        """
        return \
            (os.path.join(path, name) for path, subdirs, files in os.walk(profiles_path) for name in files)

    @staticmethod
    def __meta_file(base_path):
        """
        Extracts the metafiles.

        :param profiles_path: Path to the data-directory of the current ArgoFloat.
        :return: Generator  - Full path of the metafile in the directory.
        """
        return \
            os.path.join(
                base_path, [file for file in os.listdir(base_path) if file.endswith('_meta.nc')][0]
            )

    @staticmethod
    def __extract_float_data(file_paths):
        """
        Extract the measurement data of the current ArgoFloat.

        :param file_paths: Full paths of all files for current ArgoFloat
        :return: generator - LazyLoading-Graph holding the datarepresentations.
        """
        return \
            (FloatDataset(p) for p in file_paths
             # Don use the control and metafiles.
             if not any([pattern in p for pattern in ('_prof', '_meta', '_tech', '_Rtraj')]))

    def __extract_meta_data(self, file_path):
        """
        Extract the metadata of the current ArgoFloat.

        :param file_path: Full path to the meta data file of the current ArgoFloat.
        """
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
