from constant_umpp import *
from pylab import *
import sys
from calculate_cs2006_timescale import *

def post_process_control(varname,var,p,plot_type):

  # CO as percent of total carbon gas
  if varname=='co_as_percent':
    if verbose:
      print 'Requested variable is CO as percent of carbon gas'
    var = calc_co_as_percent(var)
  # CH4 as percent of total carbon gas
  elif varname=='ch4_as_percent':
    if verbose:
      print 'Requested variable is CH4 as percent of carbon gas'
    var = calc_ch4_as_percent(var)
  # CO mole fraction
  elif varname=='co_mole_fraction':
    if verbose:
      print 'Requested variable is CO mole fraction'
      # Do nothing
  # CH4 mole fraction
  elif varname=='ch4_mole_fraction':
    if verbose:
      print 'Requested variable is CH4 mole fraction'
      # Do nothing
  elif varname=='h2o_mole_fraction':
    if verbose:
      print 'Requested variable is H2O mole fraction'
      # Do nothing
  elif varname=='h2_mole_fraction':
    if verbose:
      print 'Requested variable is H2 mole fraction'
      # Do nothing
  elif varname=='he_mole_fraction':
    if verbose:
      print 'Requested variable is He mole fraction'
      # Do nothing
  elif varname=='n2_mole_fraction':
    if verbose:
      print 'Requested variable is N2 mole fraction'
      # Do nothing
  elif varname=='nh3_mole_fraction':
    if verbose:
      print 'Requested variable is NH3 mole fraction'
      # Do nothing
  # Half life
  elif varname=='half_life1' or varname=='half_life2':
    if verbose:
      print 'Requested variable is half life tracer'
    # Don't need to do anything for half life
  # zonal wind
  elif varname=='u':
    if verbose:
      print 'Requested variable is zonal wind'
    var = calc_wind(var)
  elif varname=='v':
    if verbose:
      print 'Requested variable is merdional wind'
    var = calc_wind(var)
  elif varname=='w':
    if verbose:
      print 'Requested variable is vertical wind'
    # Do nothing
  # temperature
  elif varname=='temp':
    if verbose:
      print 'Requested variable is temperature'
      # Don't need to do anything foz sonal wind
  # u component of dynamical timecal
  elif varname=='u_timescale':
    if verbose:
      print 'Requested variable is u component of dynamical timescale'
    var = calc_zonal_dyn_timescale(var)
  elif varname=='v_timescale':
    if verbose:
      print 'Requested variable is v component of dynamical timescale'
    var = calc_merid_dyn_timescale(var)
  elif varname=='w_timescale':
    if verbose:
      print 'Requested variable is w component of dynamical timescale'
    var = calc_vert_dyn_timescale(var)
  elif varname=='cs2006_timescale':
    if verbose:
      print 'Requested variable is Cooper and Showman 2006 chemical timescale'
    var = calc_cs2006_ts(var,p,plot_type)
  
  else:
    print 'Error: post_process_control'
    print '  variable not defined'
    sys.exit()

  return var

# Compute the CO abundance as a percent of the total carbon
def calc_co_as_percent(var):

  # Calculate CO as a percent via : CO(%) = Xco/carbon
  carbon = 4.570e-4
  var = var/carbon

  # convert to percent
  var = var*100.

  if verbose:
    print 'Calculated fraction of carbon in CO: ', carbon

  return var

# Compute the CH4 abundance as a percent of the total carbon
def calc_ch4_as_percent(var):

  # Calculate CH4 as a percent via : CH4(%) = Xch4/carbon
  carbon = 4.570e-4
  var = var/carbon

  # convert to percent
  var = var*100.

  if verbose:
    print 'Calculated fraction of carbon in CH4: ', carbon

  return var
  
def calc_wind(var):

  var = var*1.0e-3 # ms-1 -> kms-1
  
  if verbose:
    print 'Calculated wind velocity in kms-1'
  
  return var

# Calculate horizontal dynamical timescale from wind velocity
def calc_zonal_dyn_timescale(var):

  L = 2.*pi*rp_hd209 # approx planet radius (m)

  if 0. in var:
    var[var==0] = 1e-10
    if verbose:
      print 'Warning: replaced zeros in wind field with 1e-10'

  # Timescale = L/u or L/v
  var = abs(L/var)
  
  if verbose:
    print 'Calculated horizontal dynamical timescale in s'
  
  return var
  
# Calculate meridioanl dynamical timescale from wind velocity
def calc_merid_dyn_timescale(var):

  L = pi*rp_hd209/2. # approx planet radius (m)

  if 0. in var:
    var[var==0] = 1e-10
    if verbose:
      print 'Warning: replaced zeros in wind field with 1e-10'

  # Timescale = L/u or L/v
  var = abs(L/var)
  
  if verbose:
    print 'Calculated horizontal dynamical timescale in s'
  
  return var
  
# Calculate vertical dynamical timescale from wind velocity
def calc_vert_dyn_timescale(var):

  H = 1.0e5 # approx atmosphere scale height (m)
  
  # Replace zeros with small number
  if 0. in var:
    var[var==0] = 1e-10
    if verbose:
      print 'Warning: replaced zeros in wind field with 1e-10'
      
  # Timescale = H/w
  var = H/abs(var)
  
  if verbose:
    print 'Calculated vertical dynamical timescale in s'
  
  return var
  
# Calculate Cooper and Showman 2006 timescale
def calc_cs2006_ts(var,p,plot_type):

  if plot_type=='latitude_longitude':
    var1d = var.flatten()
    p1d   = zeros(var1d.size)
    p1d[:] = p
	
	  # Call CS2006 script
    ts1d = compute_timescale(p1d,var1d)
    
    # Return variable to 2D array
    var = reshape(ts1d,var.shape)

  elif plot_type=='zonal_mean' or plot_type=='pressure_latitude':

    varnew = zeros(var.shape)
    ncolumns = var.shape
    ncolumns = ncolumns[1]
    
    for i in range(ncolumns):
      varnew[:,i] = compute_timescale(p,var[:,i])
    var = varnew
    
    

  else:
    print 'Error: calc_cs2006_ts'
    print ' plot_type',plot_type,'not implemented'
    sys.exit()
  
  if verbose:
    print 'Calculated Cooper and Showman 2006 chemical timescale'
  
  return var
  
  



