import datetime

import numpy as np


from netCDF4 import Dataset


class DatasetContextManager(object):
    def __init__(self, file_path):
        self.ds = Dataset(file_path)

    def __enter__(self):
        return self.ds

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ds.close()


class FloatDataset(object):
    def __init__(self, file_path):
        with DatasetContextManager(file_path) as ds:
            #: HELPER FUNCTIONS

            #: Ease the extraction of parameter Data
            #: In some cases, some attribues are not in every dataset.
            def variables_(x):
                if x not in ds.variables:
                    return np.nan
                return np.ma.getdata(ds.variables[x][:])[0]

            #: Average if a is np.array else do nothing
            def average_(a):
                if type(a) is not np.ndarray:
                    return a
                return np.average(a)

            #: IDENTIFIER
            self.float_identifier = variables_('PLATFORM_NUMBER')
            self.cycle_number = variables_('CYCLE_NUMBER')
            # DONE @ Docs julday (seite 22 user manual)

            self.date_creation = datetime.datetime.strptime('1950-01-01', "%Y-%m-%d") + datetime.timedelta(
                days=int(variables_('JULD')))

            #: DIMENSIONS
            self.n_param = ds.dimensions['N_PARAM'].size

            #: DATA
            self.position = {'latitude': variables_('LATITUDE'),
                             'longitude': variables_('LONGITUDE')}
            self.pressure = average_(variables_('PRES'))
            self.temperature = average_(variables_('TEMP'))
            self.salinity = average_(variables_('PSAL'))
            self.conductivity = average_(variables_('CNDC'))

    def __repr__(self):
        return \
            f"""
            This is a dataset from Argo float {self.float_identifier} 
            created {self.date_creation} on the {self.cycle_number}th circle.
            """
