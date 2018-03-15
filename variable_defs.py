import sys

def get_variable_to_read(varname):

  if varname=='co_as_percent':
    varread = 'unspecified_1'
  elif varname=='ch4_as_percent':
    varread = 'unspecified_2'
  elif varname=='co_mole_fraction':
    varread = 'unspecified_1'
  elif varname=='ch4_mole_fraction':
    varread = 'unspecified_2'
  elif varname=='h2o_mole_fraction':
    varread = 'unspecified_3'
  elif varname=='half_life':
    varread = 'unspecified'
  elif varname=='u':
    varread = 'u'
  elif varname=='v':
    varread = 'v'
  elif varname=='w':
    varread = 'dz_dt'
  elif varname=='temp':
    varread = 'temp'
  # u component of dynamical timescale
  elif varname=='u_timescale':
    varread='u'
  # v component of dynamical timescale
  elif varname=='v_timescale':
    varread='v'
  # w component of dynamical timescale
  elif varname=='w_timescale':
    varread='dz_dt'
  elif varname=='cs2006_timescale':
    varread='temp'
  
  
  else:
    print 'Error: get_variable_to_read'
    print '  variable is not defined'
    sys.exit()

  return varread
