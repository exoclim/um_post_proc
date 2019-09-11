# Module to calculate variable (1D version)
# Looks for requested variable, reads in necessary data and calculates 
from construct_variable import *
from constant_user import *

# ---------------------------------------------
# Main function to calculate requested variable
# ---------------------------------------------
def calculate_variable_1d(fname,fname_keys,fname_spec,varname,time_1,time_2,lat_min,lat_max,
  lon_min,lon_max,plot_type,pressure_grid,vardim,instrument,nband):

  if varname=='temp':
    if verbose:
      read_message(varname)
    y, var = construct_variable_1d(fname,fname_keys,fname_spec,varname,time_1,time_2,
      lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid,vardim,instrument,nband)

  elif varname=='ch4_mole_fraction':
    if verbose:
      read_message(varname)
    y, var = construct_variable_1d(fname,fname_keys,fname_spec,varname,time_1,time_2,
      lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid,vardim,instrument,nband)
      
  elif varname=='h2o_mole_fraction':
    if verbose:
      read_message(varname)
    y, var = construct_variable_1d(fname,fname_keys,fname_spec,varname,time_1,time_2,
      lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid,vardim,instrument,nband)
      
  elif varname=='co_mole_fraction':
    if verbose:
      read_message(varname)
    y, var = construct_variable_1d(fname,fname_keys,fname_spec,varname,time_1,time_2,
      lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid,vardim,instrument,nband)
      
  elif varname=='co2_mole_fraction':
    if verbose:
      read_message(varname)
    y, var = construct_variable_1d(fname,fname_keys,fname_spec,varname,time_1,time_2,
      lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid,vardim,instrument,nband)
      
  elif varname=='hcn_mole_fraction':
    if verbose:
      read_message(varname)
    y, var = construct_variable_1d(fname,fname_keys,fname_spec,varname,time_1,time_2,
      lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid,vardim,instrument,nband)
      
  elif varname=='n2_mole_fraction':
    if verbose:
      read_message(varname)
    y, var = construct_variable_1d(fname,fname_keys,fname_spec,varname,time_1,time_2,
      lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid,vardim,instrument,nband)

  elif varname=='nh3_mole_fraction':
    if verbose:
      read_message(varname)
    y, var = construct_variable_1d(fname,fname_keys,fname_spec,varname,time_1,time_2,
      lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid,vardim,instrument,nband)

  elif varname=='oh_mole_fraction':
    if verbose:
      read_message(varname)
    y, var = construct_variable_1d(fname,fname_keys,fname_spec,varname,time_1,time_2,
      lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid,vardim,instrument,nband)
      
  elif varname=='h_mole_fraction':
    if verbose:
      read_message(varname)
    y, var = construct_variable_1d(fname,fname_keys,fname_spec,varname,time_1,time_2,
      lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid,vardim,instrument,nband)

  elif varname=='u_timescale':
    if verbose:
      read_message(varname)
    y, var = get_u_timescale(fname,fname_keys,fname_spec,varname,time_1,time_2,
      lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid,vardim,instrument,nband)

  elif varname=='v_timescale':
    if verbose:
      read_message(varname)
    y, var = get_v_timescale(fname,fname_keys,fname_spec,varname,time_1,time_2,
      lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid,vardim,instrument,nband)

  elif varname=='w_timescale':
    if verbose:
      read_message(varname)
    y, var = get_w_timescale(fname,fname_keys,fname_spec,varname,time_1,time_2,
      lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid,vardim,instrument,nband)

  else:
    print 'Error: calculate_variable_1d'
    print '  variable not implemented: ',varname
    exit()

  return y, var

# ---------------------------------------------
# Function to calculate zonal dynamical timescale [s]
# Requires user constants (in constant_user.py): planet radius
# ---------------------------------------------
def get_u_timescale(fname,fname_keys,fname_spec,varname,time_1,time_2,lon_request,lat_min,lat_max,
  level,plot_type,pressure_grid,vardim,instrument,nband):

  # Get zonal wind velocity
  x, var = construct_variable_1d(fname,fname_keys,fname_spec,'u',time_1,time_2,lon_request,lat_min,lat_max,
  level,plot_type,pressure_grid,vardim,instrument,nband)

  # Calculate timescale
  var = 2.*pi*Rp/abs(var)

  return x, var

# ---------------------------------------------
# Function to calculate meridional dynamical timescale [s]
# Requires user constants (in constant_user.py): planet radius
# ---------------------------------------------
def get_v_timescale(fname,fname_keys,fname_spec,varname,time_1,time_2,lon_request,lat_min,lat_max,
  level,plot_type,pressure_grid,vardim,instrument,nband):

  # Get meridional wind velocity
  x, var = construct_variable_1d(fname,fname_keys,fname_spec,'v',time_1,time_2,lon_request,lat_min,lat_max,
  level,plot_type,pressure_grid,vardim,instrument,nband)

  # Calculate timescale
  var = pi*Rp/abs(var)/2.

  return x, var

# ---------------------------------------------
# Function to calculate vertical dynamical timescale [s]
# Requires user constants (in constant_user.py): surface gravity, mean molecular mass
# ---------------------------------------------
def get_w_timescale(fname,fname_keys,fname_spec,varname,time_1,time_2,lon_request,lat_min,lat_max,
  level,plot_type,pressure_grid,vardim,instrument,nband):

  # Get vertical wind velocity
  x, w = construct_variable_1d(fname,fname_keys,fname_spec,'w',time_1,time_2,lon_request,lat_min,lat_max,
  level,plot_type,pressure_grid,vardim,instrument,nband)

  #Get temperature
  x, temp = construct_variable_1d(fname,fname_keys,fname_spec,'temp',time_1,time_2,lon_request,lat_min,lat_max,
  level,plot_type,pressure_grid,vardim,instrument,nband)

  # Calculate scale height
  H = kb*temp/(mu*amu*surf_gravity)

  # Calculate timescale
  var = H/abs(w)

  return x, var

def read_message(varname):
  print 'Routine: calculate_variable_1d'
  print '  requested variable is: ',varname
