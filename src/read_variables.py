import netCDF4 as nc
from constant_umpp import *
from pylab import *
import sys

# Read variable on 3D grid + time
def read_variable_4d(fname,varname):

  # Open netcdf file
  data = nc.Dataset(fname,'r')
 
  # Read variable dimensions
  dims      = data.variables[varname].dimensions
  time      = data.variables[dims[0]][:]
  height    = data.variables[dims[1]][:]
  latitude  = data.variables[dims[2]][:]
  longitude = data.variables[dims[3]][:]

  # Read variable
  variable = data.variables[varname][:,:,:,:]

  if verbose:
    print 'Read variable: ', varname
    print '  ntime: ', time.size
    print '  nheight: ', height.size
    print '  nlongitude: ', longitude.size
    print '  nlatitude: ', latitude.size
    print '  max var:   ', amax(variable)
    print ', min var:   ', amin(variable)

  return time, height, longitude, latitude, variable

def read_netcdf_keys(fname,varname):

  # Read netcdf keys to get netcdf variable name
  keys = genfromtxt(fname,dtype='str',delimiter=' ')
  
  # Number of keys
  nkeys = len(keys)
  
  # Get requested netcdf variable name
  for i in range(nkeys):
    if keys[i,0]==varname:
      varread = keys[i,1]
      
  return varread