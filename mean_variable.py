from pylab import *
import sys
from constant_umpp import *

# Take the temporal mean of a 4D array

def mean_lim(
# dimension of variable to be averaged
dim,
# variable
variable,
# minimum limit for mean
lim_min,
# maximum limit for mean
lim_max,
# axis on which to perform mean
axis):

  # Check that requested limits are in range of data
  if min(dim)>lim_min:
    print 'Error: mean_lim'
    print 'requested minimum limit below range of data'
    print 'lim_min: ', lim_min, 'minimum in data: ',min(dim)
    sys.exit()
  elif max(dim)<lim_max:
    print 'Error: mean_lim'
    print 'requested maximum limit above range of data'
    print 'lim_max: ', lim_max, 'maximum in data: ',max(dim)
    sys.exit()

  # Get closest indices to requested limits
  imin = argmin(abs(dim-lim_min))
  imax = argmin(abs(dim-lim_max))

  # Perform temporal mean
  var_mean = mean(variable[imin:imax,:,:,:],axis=axis)

  if verbose: 
    print 'Temporal mean of variable'
    print '  time_min: ', lim_min, 'time_max: ', lim_max
    print '  max value: ', amax(var_mean), ' min value: ', amin(var_mean)

  return var_mean
 
def mean_var(
var,
axis):

  # Perform mean
  var_mean = mean(var,axis)

  if verbose:
    print 'Performed mean of variable along axis: ',axis

  return var_mean 

def spatial_mean_weight_lim(dim,variable,weights,axis):

   # Perform weighted mean
  var_mean = average(variable,axis=axis,weights=weights)

  return var_mean
