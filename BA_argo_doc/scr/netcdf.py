from netCDF4 import Dataset

dataset = Dataset('./D5900739_100.nc')
lat = dataset.variables['LATITUDE'][:][0]
lon = dataset.variables['LONGITUDE'][:][0]
dataset.close()

print(f"( {lat}, {lon} )")
# ( 22.495, -171.791 )

