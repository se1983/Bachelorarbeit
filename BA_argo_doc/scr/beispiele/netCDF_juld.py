from netCDF4 import Dataset
import datetime

dataset = Dataset('./4900442/profiles/D4900442_042.nc')
print(dataset.variables['JULD'])

# <class 'netCDF4._netCDF4.Variable'>
# float64 JULD(N_PROF)
#     long_name: Julian day (UTC) of the station relative to REFERENCE_DATE_TIME
#     units: days since 1950-01-01 00:00:00 UTC
#     conventions: Relative julian days with decimal part (as parts of day)
#     _FillValue: 999999.0
# unlimited dimensions: 
# current shape = (1,)
# filling off

julian_date = dataset.variables['JULD'][::][0]
dataset.close()

print(julian_date)
# 20062.5483218

juld_zero = datetime.datetime.strptime( '1950-01-01 00:00:00 UTC', 
                                          '%Y-%m-%d %H:%M:%S UTC')
date_creation = juld_zero + datetime.timedelta(days=int(julian_date))
print(date_creation)
# datetime.datetime(2004, 12, 5, 0, 0)


