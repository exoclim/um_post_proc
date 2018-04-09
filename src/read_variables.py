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

# Read variable on 3D grid + time + bands
def read_variable_5d(fname,varname):

  # Open netcdf file
  data = nc.Dataset(fname,'r')

  # Read variable dimensions
  dims      = data.variables[varname].dimensions
  time      = data.variables[dims[0]][:]
  height    = data.variables[dims[1]][:]
  latitude  = data.variables[dims[2]][:]
  longitude = data.variables[dims[3]][:]
  band      = data.variables[dims[4]][:]

  # Read variable
  variable = data.variables[varname][:,:,:,:,:]

  if verbose:
    print 'Read variable: ', varname
    print '  ntime: ', time.size
    print '  nheight: ', height.size
    print '  nlongitude: ', longitude.size
    print '  nlatitude: ', latitude.size
    print '  nband:     ', band.size
    print '  max var:   ', amax(variable)
    print ', min var:   ', amin(variable)

  return time, height, longitude, latitude, band, variable

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

def read_spectral_wavelength(fname,nband):

  # Waveband limits
  wvmin = []
  wvmax = []

  f = open(fname, 'r')

  band_block = True
  while band_block:
    line = f.readline()
    line = line.strip()
    columns = line.split()

    if columns[0]=='Band':
      band_block = False 

  # Read waveband limits
  for i in range(nband):
    line = f.readline()
    line = line.strip()
    columns = line.split()

    wvmin.append(columns[1])
    wvmax.append(columns[2])

  # Convert list to np array
  wvmin = np.asarray(wvmin)
  wvmax = np.asarray(wvmax)

  # Convert string to float
  wvmin = wvmin.astype(np.float)
  wvmax = wvmax.astype(np.float)

  return wvmin, wvmax
  
