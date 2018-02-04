import datetime

import numpy as np

from ._data_set_context_manager import DatasetContextManager


class FloatDataset(object):
    def __init__(self, file_path):
        with DatasetContextManager(file_path) as ds:
            #: HELPER FUNCTIONS

            #: Ease the extraction of parameter Data
            #: In some cases, some attribues are not in every dataset.
            def variables_(x):
                if x not in ds.variables:
                    return np.nan
                return np.ma.getdata(ds.variables[x][:])

            #: Average if a is np.array else do nothing
            def average_(a):
                if type(a) is not np.ndarray:
                    return a
                return np.average(a)

            #: IDENTIFIER
            self.float_identifier = variables_('PLATFORM_NUMBER')[0]
            self.cycle_number = variables_('CYCLE_NUMBER')[0]

            self.date_creation = datetime.datetime.strptime('1950-01-01', "%Y-%m-%d") + \
                                 datetime.timedelta(days=int(variables_('JULD')[0]))

            #: DIMENSIONS
            self.n_param = ds.dimensions['N_PARAM'].size

            #: DATA
            self.position = {'latitude': variables_('LATITUDE')[0],
                             'longitude': variables_('LONGITUDE')[0]}
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
