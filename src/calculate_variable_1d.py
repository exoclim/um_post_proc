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

  else:
    print 'Error: calculate_variable_1d'
    print '  variable not implemented: ',varname
    exit()

  return y, var

def read_message(varname):
  print 'Routine: calculate_variable_1d'
  print '  requested variable is: ',varname