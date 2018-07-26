# Module to calculate variable 
# Looks for requested variable, reads in necessary data and calculates 
from construct_variable import *
from constant_user import *

# ---------------------------------------------
# Main function to calculate requested variable
# ---------------------------------------------
def calculate_variable(fname,fname_keys,fname_spec,varname,time_1,time_2,lon,lat_min,lat_max,
  level,plot_type,pressure_grid,vardim,instrument,nband):

  print "HELLO"
  print varname

  # Zonal wind
  if varname=='u':
    if verbose:
      print 'Requested variable is zonal wind'
    x, y, var = construct_variable_2d(fname,fname_keys,fname_spec,varname,time_1,time_2,lon,lat_min,lat_max,
    level,plot_type,pressure_grid,vardim,instrument,nband)
  
  # Meridional wind
  elif varname=='v':
    if verbose:
      print 'Requested variable is meridional wind'
    x, y, var = construct_variable_2d(fname,fname_keys,fname_spec,varname,time_1,time_2,lon,lat_min,lat_max,
    level,plot_type,pressure_grid,vardim,instrument,nband)
  
  # Vertical wind
  elif varname=='w':
    if verbose:
      print 'Requested variable is vertical wind'
    x, y, var = construct_variable_2d(fname,fname_keys,fname_spec,varname,time_1,time_2,lon,lat_min,lat_max,
    level,plot_type,pressure_grid,vardim,instrument,nband)
  
  # Temperature
  elif varname=='temp':
    if verbose:
      print 'Requested variable is temperature'
    x, y, var = construct_variable_2d(fname,fname_keys,fname_spec,varname,time_1,time_2,lon,lat_min,lat_max,
    level,plot_type,pressure_grid,vardim,instrument,nband)
    
  # Surface Temperature
  elif varname=='surface_temp':
    if verbose:
      print 'Requested variable is surface temperature'
    x, y, var = construct_variable_2d(fname,fname_keys,fname_spec,varname,time_1,time_2,lon,lat_min,lat_max,
    level,plot_type,pressure_grid,vardim,instrument,nband)
      
  # Methane mole fraction
  elif varname=='ch4_mole_fraction':
    if verbose:
      print 'Requested variable is methane mole fraction'
    x, y, var = construct_variable_2d(fname,fname_keys,fname_spec,varname,time_1,time_2,lon,lat_min,lat_max,
    level,plot_type,pressure_grid,vardim,instrument,nband)

  # Water mole fraction
  elif varname=='h2o_mole_fraction':
    if verbose:
      print 'Requested variable is water mole fraction'
    x, y, var = construct_variable_2d(fname,fname_keys,fname_spec,varname,time_1,time_2,lon,lat_min,lat_max,
    level,plot_type,pressure_grid,vardim,instrument,nband)

  # Carbon monoxide mole fraction
  elif varname=='co_mole_fraction':
    if verbose:
      print 'Requested variable is carbon monoxide mole fraction'
    x, y, var = construct_variable_2d(fname,fname_keys,fname_spec,varname,time_1,time_2,lon,lat_min,lat_max,
    level,plot_type,pressure_grid,vardim,instrument,nband)
  
  # Longwave heating rate in [W/m3]
  elif varname=='lwhr_wm3':
    if verbose:
      print 'Requested variable is longwave heating rate [Wm-3]'
    x, y, var = get_lwhr_wm3(fname,fname_keys,fname_spec,varname,time_1,time_2,lon,lat_min,lat_max,
    level,plot_type,pressure_grid,vardim,instrument,nband)
      
  # Shortwave heating rate in [W/m3]
  elif varname=='swhr_wm3':
    if verbose:
      print 'Requested variable is shortwave heating rate [Wm-3]'
    x, y, var = get_swhr_wm3(fname,fname_keys,fname_spec,varname,time_1,time_2,lon,lat_min,lat_max,
    level,plot_type,pressure_grid,vardim,instrument,nband)
    
  # Net heating rate in [W/m3]
  elif varname=='nethr_wm3':
    if verbose:
      print 'Requested variable is net heating rate [Wm-3]'
    x, y, var = get_nethr_wm3(fname,fname_keys,fname_spec,varname,time_1,time_2,lon,lat_min,lat_max,
    level,plot_type,pressure_grid,vardim,instrument,nband)
      
  # Radiative timescale
  elif varname=='rad_timescale':
    if verbose: 
      print 'Requested variable is radiative timescale'
    x, y, var = get_rad_timescale(fname,fname_keys,fname_spec,varname,time_1,time_2,lon,lat_min,lat_max,
    level,plot_type,pressure_grid,vardim,instrument,nband)

  # Contribution function
  elif varname=='cf':
    if verbose:
      print 'Requested variable is contribution function'
    x, y, var =  get_cf(fname,fname_keys,fname_spec,varname,time_1,time_2,lon,lat_min,lat_max,
    level,plot_type,pressure_grid,vardim,instrument,nband)

  else:
    print 'Error: calculate_variable'
    print 'variable not implemented: ',varname
    exit()
    
  return x, y, var

# ---------------------------------------------
# Function to calculate longwave heating rate [W/m3]
# ---------------------------------------------
def get_lwhr_wm3(fname,fname_keys,fname_spec,varname,time_1,time_2,lon_request,lat_min,lat_max,
  level,plot_type,pressure_grid,vardim,instrument,nband):
  
  # Read heating rates
  varname_loc = 'lwhr'
  x, y, lwhr = construct_variable_2d(fname,fname_keys,fname_spec,varname_loc,time_1,time_2,lon_request,lat_min,lat_max,
    level,plot_type,pressure_grid,vardim,instrument,nband)
  
  # Read temperature 
  varname_loc = 'temp'
  x, y, temp = construct_variable_2d(fname,fname_keys,fname_spec,varname_loc,time_1,time_2,lon_request,lat_min,lat_max,
    level,plot_type,pressure_grid,vardim,instrument,nband)
  
  # Plot type where y is pressure
  if plot_type=='meridional_mean' or plot_type=='zonal_mean' or plot_type=='pressure_latitude' or plot_type=='pressure_longitude':
    for i in range(x.size):
      # Calculate mass density from ideal gas law
      density = y/rspecific/temp[:,i]
      
      # Calculate longwave heating rate in [W/m3]
      lwhr[:,i] = lwhr[:,i]*cpspecific*density
  
  else:
    print 'Error: get_lwhr_wm3'
    print 'Plot type ', plot_type, ' not implemented'
    exit()
    
  return x, y, lwhr

# ---------------------------------------------
# Function to calculate shortwave heating rate [W/m3]
# ---------------------------------------------
def get_swhr_wm3(fname,fname_keys,fname_spec,varname,time_1,time_2,lon_request,lat_min,lat_max,
  level,plot_type,pressure_grid,vardim,instrument,nband):
  
  # Read heating rates
  varname_loc = 'swhr'
  x, y, swhr = construct_variable_2d(fname,fname_keys,fname_spec,varname_loc,time_1,time_2,lon_request,lat_min,lat_max,
    level,plot_type,pressure_grid,vardim,instrument,nband)
  
  # Read temperature 
  varname_loc = 'temp'
  x, y, temp = construct_variable_2d(fname,fname_keys,fname_spec,varname_loc,time_1,time_2,lon_request,lat_min,lat_max,
    level,plot_type,pressure_grid,vardim,instrument,nband)
  
  # Plot type where y is pressure
  if plot_type=='meridional_mean' or plot_type=='zonal_mean' or plot_type=='pressure_latitude' or plot_type=='pressure_longitude':
    for i in range(x.size):
      # Calculate mass density from ideal gas law
      density = y/rspecific/temp[:,i]
      
      # Calculate longwave heating rate in [W/m3]
      swhr[:,i] = swhr[:,i]*cpspecific*density
  
  else:
    print 'Error: get_swhr_wm3'
    print 'Plot type ', plot_type, ' not implemented'
    exit()
    
  return x, y, swhr

# ---------------------------------------------
# Function to calculate net heating rate [W/m3]
# ---------------------------------------------
def get_nethr_wm3(fname,fname_keys,fname_spec,varname,time_1,time_2,lon_request,lat_min,lat_max,
  level,plot_type,pressure_grid,vardim,instrument,nband):
  
  # Get shortwave heating rate
  x, y, swhr = get_swhr_wm3(fname,fname_keys,fname_spec,varname,time_1,time_2,lon_request,lat_min,lat_max,
  level,plot_type,pressure_grid,vardim,instrument,nband)

  # Get longwave heating rate
  x, y, lwhr = get_lwhr_wm3(fname,fname_keys,fname_spec,varname,time_1,time_2,lon_request,lat_min,lat_max,
  level,plot_type,pressure_grid,vardim,instrument,nband)
  
  # Calculate net heating rate
  nethr = swhr + lwhr
  
  return x, y, nethr
  
# ---------------------------------------------
# Function to calculate radiative timescale [s] from Showman and Guillot 2002, Eq 10
# ---------------------------------------------
def get_rad_timescale(fname,fname_keys,fname_spec,varname,time_1,time_2,lon_request,lat_min,lat_max,
  level,plot_type,pressure_grid,vardim,instrument,nband):
  
  # Read temperature
  varname_loc = 'temp'
  x, y, temp = construct_variable_2d(fname,fname_keys,fname_spec,varname_loc,time_1,time_2,lon_request,lat_min,lat_max,
    level,plot_type,pressure_grid,vardim,instrument,nband)

  # Define new variable array
  var = zeros((y.size,x.size))

  # Plot type where y is pressure
  if plot_type=='meridional_mean' or plot_type=='zonal_mean' or plot_type=='pressure_latitude' or plot_type=='pressure_longitude':
    for i in range(x.size):
      var[:,i] = surface_gravity*4.*sigma*temp[:,i]**3
      var[:,i] = y*cpspecific/var[:,i]
      
  else:
    print 'Error: get_swhr_wm3'
    print 'Plot type ', plot_type, ' not implemented'
    exit()
    
  return x, y, var
  
# ---------------------------------------------
# Function to calculate normalised contribution function
# ---------------------------------------------

def get_cf(fname,fname_keys,fname_spec,varname,time_1,time_2,lon_request,lat_min,lat_max,
  level,plot_type,pressure_grid,vardim,instrument,nband):

  # Read contribution function
  x, y, cf = construct_variable_2d(fname,fname_keys,fname_spec,varname,time_1,time_2,lon_request,lat_min,lat_max,
    level,plot_type,pressure_grid,vardim,instrument,nband)

  if plot_type=='zonal_mean' or plot_type=='meridional_mean' or plot_type=='pressure_longitude':
    # Assume pressure is first dimension
    dims = cf.shape
    var = zeros(dims)

    for i in range(dims[1]):
      var[:,i] = cf[:,i]/amax(cf[:,i])
  else:
    var = cf/amax(cf)

  return x, y, var


