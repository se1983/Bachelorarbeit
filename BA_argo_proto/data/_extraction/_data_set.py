import datetime

import numpy as np

from ._data_set_context_manager import DatasetContextManager
from ._extract_dataset import extract_variable


class FloatDataset(object):
    def __init__(self, file_path):
        with DatasetContextManager(file_path) as ds:
            #: HELPER FUNCTIONS

            #: Ease the extraction of parameter Data
            #: In some cases, some attribues are not in every dataset.

            #: Average if a is np.array else do nothing
            def average_(a):
                if type(a) is not np.ndarray:
                    return a
                return np.average(a)

            #: IDENTIFIER
            self.cycle_number = extract_variable(ds, 'CYCLE_NUMBER')[0]

            juld = extract_variable(ds, 'JULD')[0]
            self.date_creation = datetime.datetime.strptime('1950-01-01', "%Y-%m-%d") + datetime.timedelta(
                days=int(juld))

            #: DATA
            self.position = {
                'latitude': np.float(extract_variable(ds, 'LATITUDE')[0]),
                'longitude': np.float(extract_variable(ds, 'LATITUDE')[0])
            }
            self.pressure = np.average(extract_variable(ds, 'PRES'))
            self.temperature = np.average(extract_variable(ds, 'TEMP'))
            self.salinity = np.average(extract_variable(ds, 'PSAL'))

            self.valid_data_ranges = self.__check_data()

    def __repr__(self):
        return \
            f"""
            This is a dataset from Argo float {self.float_identifier} 
            created {self.date_creation} on the {self.cycle_number}th circle.
            """

    def __check_data(self):
        # See argo-data documentation
        ranges = {
            'pressure': (0, 12000),
            'temperature': (-2, 40),
            'salinity': (0, 42)
        }

        return (
                ranges['pressure'][0] <= self.pressure <= ranges['pressure'][1] and
                ranges['temperature'][0] <= self.temperature <= ranges['temperature'][1] and
                ranges['salinity'][0] <= self.salinity <= ranges['salinity'][1]
        )
