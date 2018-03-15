import netCDF4 as nc
from constant_umpp import *
import os
import sys

def save_var_3d(save_dir,fname,x,y,z,f):

  # Check if directory exists
  if os.path.exists(save_dir+'saved_vars') == False:
    # Create saved_vars directory
    os.makedirs(save_dir+'saved_vars')

  # Open file
  fout = nc.Dataset(save_dir+'saved_vars/'+fname,'w')

  # Create dimensions
  nx = x.size
  ny = y.size
  nz = z.size
  fout.createDimension('x',nx)
  fout.createDimension('y',ny)
  fout.createDimension('z',nz)

  # Create variable
  varout = fout.createVariable('variable','f8',('z','y','x'))
  xout   = fout.createVariable('x','f8',('x'))
  yout   = fout.createVariable('y','f8',('y'))
  zout   = fout.createVariable('z','f8',('z'))

  # Copy variable
  varout[:,:,:] = f
  xout[:]     = x
  yout[:]     = y
  zout[:]     = z

  fout.close()

def save_var_2d(save_dir,fname,x,y,f):

  # Check if directory exists
  if os.path.exists(save_dir+'saved_vars') == False:
    # Create saved_vars directory
    os.makedirs(save_dir+'saved_vars')

  # Open file
  fout = nc.Dataset(save_dir+'saved_vars/'+fname,'w')

  # Create dimensions
  nx = x.size
  ny = y.size
  fout.createDimension('x',nx)
  fout.createDimension('y',ny)

  # Create variable
  varout = fout.createVariable('variable','f8',('y','x'))
  xout   = fout.createVariable('x','f8',('x'))
  yout   = fout.createVariable('y','f8',('y'))

  # Copy variable
  varout[:,:] = f
  xout[:]     = x
  yout[:]     = y 

  fout.close()

  if verbose:
    print 'Saved variable at : ',fname

# Save constructed variable to netcdf file
def save_var_1d(save_dir,fname,x,f):

  # Check if directory exists
  if os.path.exists(save_dir+'saved_vars') == False:
    # Create saved_vars directory
    os.makedirs(save_dir+'saved_vars')

  # Open file
  fout = nc.Dataset(save_dir+'saved_vars/'+fname,'w')

  # Create Dimensions
  nx = x.size
  fout.createDimension('x',nx)

  # Create variable
  varout = fout.createVariable('variable','f8',('x'))
  xout   = fout.createVariable('x','f8',('x'))

  # Copy variables
  varout[:] = f
  xout[:]   = x

  fout.close()

  if verbose:
    print 'Saved variable at : ', fname+'_saved_var'

def read_saved_var_3d(save_dir,fname):

  # Open file
  fin  = nc.Dataset(save_dir+'saved_vars/'+fname,'r')

  # Read dimensions
  dims = fin.variables['variable'].dimensions
  x    = fin.variables[dims[0]][:]
  y    = fin.variables[dims[1]][:]
  z    = fin.variables[dims[2]][:]

  # Read variable
  f    = fin.variables['variable'][:,:]

  print 'Read saved variable from file: ',fname+'_saved_var'

  return x, y, z, f 

def read_saved_var_2d(save_dir,fname):

  # Open file
  fin  = nc.Dataset(save_dir+'saved_vars/'+fname,'r')

  # Read dimensions
  dims = fin.variables['variable'].dimensions
  x    = fin.variables[dims[0]][:]
  y    = fin.variables[dims[1]][:]

  # Read variable
  f    = fin.variables['variable'][:,:]

  print 'Read saved variable from file: ',fname+'_saved_var'

  return x, y, f 

# Read saved variable 1D
def read_saved_var_1d(save_dir,fname):

    # Open file
  fin  = nc.Dataset(save_dir+'saved_vars/'+fname,'r')

  # Read dimensions
  dims = fin.variables['variable'].dimensions
  x    = fin.variables[dims[0]][:]

  # Read variable
  f    = fin.variables['variable'][:]

  print 'Read saved variable from file: ',fname+'_saved_var'

  return x, f

