from pylab import *
from read_variables import *
from scipy.interpolate import *
from constant_umpp import *
import sys

# Function to return linear interpolation of 1D array
def linear_interp_1d(x,x2,z):

  f  = interp1d(x,z)
  z2 = f(x2)

  return z2 

def linear_interp_2d(x,x2,y,y2,z):

  f = interp2d(x,y,z)
  z2 = f(x2,y2)
 
  x2, y2 = meshgrid(x2,y2)

  return z2

def cubic_interp_2d(x,x2,y,y2,z):

  f = interp2d(x,y,z,kind='cubic')
  z2 = f(x2,y2)

  x2, y2 = meshgrid(x2,y2)

  return z2
  
def linear_extrap_1d(x,x2,z):

  z2 = zeros(z.size+2)
  x3 = zeros(z.size+2)
  
  z2[1:-1] = z
  x3[1:-1] = x
  
  z2[0]  = z[0] + (x2[0]-x[0])/(x[1]-x[0])*(z[1]-z[0])
  x3[0]  = x2[0]
  z2[-1] = z[-1] + (x2[-1]-x[-1])/(x[-2]-x[-1])*(z[-2]-z[-1])
  x3[-1] = x2[-1]
  
  return x3, z2

# Get a variable on the pressure grid
def interpolate_on_p_profile_time(time_var,height_var,lat_var,lon_var,var,time_1,time_2,fname):

	# Read pressure grid
	time_p, height_p, lon_p, lat_p, p = read_variable_4d(fname,varname='p')
	
  # Get size of dimensions
	ntime = time_var.size
	nlon = lon_var.size
	nlat  = lat_var.size
	nheight = height_var.size
	
	ntime_p = time_p.size
	nlon_p = lon_p.size
	nlat_p = lat_p.size
	nheight_p = height_p.size
	
	# Check if variable and pressure grids are different
	var = check_variable_pressure_grid(ntime,nlon,nlat,nheight,time_var,height_var,lon_var,lat_var,
	                                 ntime_p,nlon_p,nlat_p,nheight_p,time_p,height_p,lon_p,lat_p,
	                                 var,p)

	# Cut time axis
	index = index = array(where((time_p>=time_1) & (time_p<=time_2))).flatten()
	p = p[index,:,:,:]
	time_p = time_p[index]
	var = var[index]

	if verbose:
		print 'Interpolating variable onto pressure grid for time in range'
		print '  time_min: ', time_var[0], 'time_max: ', time_var[-1]

	# Update size of dimensions
	ntime = time_p.size
	nlon = lon_p.size
	nlat  = lat_p.size
	nheight = height_var.size
	
	# Invert height dimension
	p = p[:,::-1,:,:]
	var = var[:,::-1,:,:]

	pvargrid = zeros((ntime,nheight,nlat,nlon))

	# Find pressure values on variable height grid
	for itime in range(ntime):
		print 'time: ',itime+1,'/',ntime
		# Loop over longitudes
		for ilon in range(nlon):
			# Loop over latitudes
			for ilat in range(nlat):
				# Get pressure on variable height grid
				pvargrid[itime,:,ilat,ilon] = linear_interp_1d(height_p,height_var,p[itime,:,ilat,ilon])

	# Compute new uniform P grid
	pmin = amax(pvargrid[:,0,:,:])*1.00001
	pmax = amin(pvargrid[:,-1,:,:])/1.00001   
	pnew = logspace(log10(pmax),log10(pmin),nheight)
	var_interp = zeros((ntime,nheight,nlat,nlon))


	# Compute variable on new pressure grid
	for itime in range(ntime):
		for ilon in range(nlon):
			for ilat in range(nlat):
				# Get variable on new pressure grid

				var_interp[itime,:,ilat,ilon] = linear_interp_1d(pvargrid[itime,:,ilat,ilon],pnew,var[itime,:,ilat,ilon])

	if verbose:
		print 'Interpolated variable onto new pressure grid:'
		print '  min: ',amin(pnew), '  max:  ', amax(pnew)

	return pnew, lat_p, lon_p, var_interp

  
def interpolate_on_p_profile(time_var,height_var,lat_var,lon_var,var,time_1,fname):

	# Read pressure grid
	time_p, height_p, lon_p, lat_p, p = read_variable_4d(fname,varname='p')

  # Get size of dimensions
	ntime = time_var.size
	nlon = lon_var.size
	nlat  = lat_var.size
	nheight = height_var.size
	
	ntime_p = time_p.size
	nlon_p = lon_p.size
	nlat_p = lat_p.size
	nheight_p = height_p.size

	# Check if variable and pressure grids are different
	var = check_variable_pressure_grid(ntime,nlon,nlat,nheight,time_var,height_var,lon_var,lat_var,
																	 ntime_p,nlon_p,nlat_p,nheight_p,time_p,height_p,lon_p,lat_p,
																	 var,p)

	# Select requested time
	itime = argmin(abs(time_var-time_1))
	p = p[itime,:,:,:]
	var = var[itime,:,:,:]

  # Update size of dimensions
	nlon = lon_p.size
	nlat  = lat_p.size
	nheight = height_var.size
	
	# Invert height dimension
	p = p[::-1,:,:]
	var = var[::-1,:,:]

	pvargrid = zeros((nheight,nlat,nlon))
	# Find pressure values on variable height grid
	# Loop over longitudes
	for ilon in range(nlon):
		# Loop over latitudes
		for ilat in range(nlat):
			# Get pressure on variable height grid
			pvargrid[:,ilat,ilon] = linear_interp_1d(height_p,height_var,p[:,ilat,ilon])

        # Compute new uniform P grid
	pmin = amax(pvargrid[0,:,:])*1.000001
	pmax = amin(pvargrid[-1,:,:])/1.00001   
	pnew = logspace(log10(pmax),log10(pmin),nheight_p)
	var_interp = zeros((nheight_p,nlat,nlon))


	# Compute variable on new pressure grid
	for ilon in range(nlon):
		for ilat in range(nlat):
			# Get variable on new pressure grid
			var_interp[:,ilat,ilon] = linear_interp_1d(pvargrid[:,ilat,ilon],pnew,var[:,ilat,ilon])

	if verbose:
		print 'Interpolated variable onto new pressure grid:'
		print '  min: ',amin(pnew), '  max:  ', amax(pnew)

	return pnew, lat_p, lon_p, var_interp
	
def interpolate_on_p_point(time_var,height_var,lat_var,lon_var,var,time_1,plevel,fname):

	# Read pressure grid
	time_p, height_p, lon_p, lat_p, p = read_variable_4d(fname,varname='p')

	ntime = time_var.size
	nlon = lon_var.size
	nlat  = lat_var.size
	nheight = height_var.size
	
	ntime_p = time_p.size
	nlon_p = lon_p.size
	nlat_p = lat_p.size
	nheight_p = height_p.size

	# Check variable and pressure grids, update p if necessary
	var = check_variable_pressure_grid(ntime,nlon,nlat,nheight,time_var,height_var,lon_var,lat_var,
																	 ntime_p,nlon_p,nlat_p,nheight_p,time_p,height_p,lon_p,lat_p,
																	 var,p)

	# Select requested time
	itime = argmin(abs(time_var-time_1))
	p = p[itime,:,:,:]
	var = var[itime,:,:,:]

	nlon = lon_p.size
	nlat = lat_p.size
	nheight = height_p.size

  
	# invert height dimension
	p = p[::-1,:,:]
	var = var[::-1,:,:]

	var_at_p = zeros((nlat,nlon))

	for ilon in range(nlon):
		for ilat in range(nlat):
			# Get pressure on variable height grid
			pvargrid = linear_interp_1d(height_p,height_var,p[:,ilat,ilon])
			# Get variable at requested pressure
			var_at_p[ilat,ilon] = linear_interp_1d(pvargrid,plevel,var[:,ilat,ilon])

	return lat_p, lon_p, var_at_p

def interpolate_on_p_point_time(time_var,height_var,lat_var,lon_var,var,plevel,fname):

	# Read pressure grid
	time_p, height_p, lon_p, lat_p, p = read_variable_4d(fname,varname='p')

	ntime = time_var.size
	nlon = lon_var.size
	nlat  = lat_var.size
	nheight = height_var.size
	
	ntime_p = time_p.size
	nlon_p = lon_p.size
	nlat_p = lat_p.size
	nheight_p = height_p.size

	# Check variable and pressure grids, update p if necessary
	var = check_variable_pressure_grid(ntime,nlon,nlat,nheight,time_var,height_var,lon_var,lat_var,
																	 ntime_p,nlon_p,nlat_p,nheight_p,time_p,height_p,lon_p,lat_p,
																	 var,p)
  
	# invert height dimension
	p = p[:,::-1,:,:]
	var = var[:,::-1,:,:]

	ntime = time_p.size
	nlon = lon_p.size
	nlat = lat_p.size
	nheight = height_p.size

	var_at_p = zeros((ntime,nlat,nlon))

	for itime in range(ntime):
		print 'time: ',itime+1,'/',ntime
		for ilon in range(nlon):
			for ilat in range(nlat):
				# Get pressure on variable height grid
				pvargrid = linear_interp_1d(height_p,height_var,p[itime,:,ilat,ilon])
				# Get variable at requested pressure
				var_at_p[itime,ilat,ilon] = linear_interp_1d(pvargrid,plevel,var[itime,:,ilat,ilon])

	return lat_p, lon_p,var_at_p

# Function to interpolate variable onto pressure longitude grid longitude
def interpolate_longitude(ntime,nheight,nlat,nlong,long_p,long_var,p,var):

  # Extend arrays using periodic boundaries
  dlon = long_p[1] - long_p[0] # assuming uniform grid
  long_p_loc = append(long_p,long_p[-1]+dlon)
  long_p_loc = long_p_loc[::-1]
  long_p_loc = append(long_p_loc,long_p[0]-dlon)
  long_p_loc = long_p_loc[::-1]

  long_var_loc = append(long_var,long_var[-1]+dlon)
  long_var_loc = long_var_loc[::-1]
  long_var_loc = append(long_var_loc,long_var[0]-dlon)
  long_var_loc = long_var_loc[::-1]

  var_interp = zeros((ntime,nheight,nlat,nlong))
  for itime in range(ntime):
    for iheight in range(nheight):
      for ilat in range(nlat):
        # First extend dimension assuming periodic boundaries
        varloc = var[itime,iheight,ilat,:]
        varloc = append(varloc,varloc[0])
        varloc = varloc[::-1]
        varloc = append(varloc,varloc[0])
        varloc = varloc[::-1]
        var_interp[itime,iheight,ilat,:] = linear_interp_1d(long_var_loc,long_p,varloc)

  if verbose:
    print 'Interpolated variable onto pressure grid'
   
  return var_interp

# Function to interpolate variable onto pressure latitude grid
def interpolate_latitude(ntime,nheight,nlat,nlon,nlat_p,lat_p,lat_var,p,var):
  
  var_interp = zeros((ntime,nheight,nlat_p,nlon))

  for itime in range(ntime):
    for iheight in range(nheight):
      for ilon in range(nlon):
        var_interp[itime,iheight,:,ilon] = linear_interp_1d(lat_var,lat_p,var[itime,iheight,:,ilon])
  
  if verbose:
    print 'Interpolated variable onto pressure latitude grid'
  
  return var_interp

# Function to interpolate in 2D 
def interpolate_latitude_longitude_2d(p_var,lon_var,lat_var,lon_request,lat_request,var):

  #First extend longitude dimension for periodic interpolate
  lon_loc = zeros(lon_var.size+2)
  dlon = lon_var[1]-lon_var[0]
  lon_loc[1:lon_var.size+1] = lon_var
  lon_loc[0] = lon_var[0] - dlon
  lon_loc[lon_var.size+1] = lon_var[lon_var.size-1]+dlon

  var_loc = zeros((p_var.size,lat_var.size,lon_var.size+2))
  var_loc[:,:,1:lon_var.size+1] = var
  var_loc[:,:,0] = var[:,:,lon_var.size-1]
  var_loc[:,:,lon_var.size+1] = var[:,:,0]
  
  # Perform 2d interpolation

  var_interp = zeros(p_var.size)

  for iheight in range(p_var.size):
    
    var_interp[iheight] = linear_interp_2d(lon_loc,lon_request,lat_var,lat_request,var_loc[iheight,:,:])

  return var_interp
  
def check_variable_pressure_grid(ntime,nlon,nlat,nheight,time_var,height_var,lon_var,lat_var,
	                                 ntime_p,nlon_p,nlat_p,nheight_p,time_p,height_p,lon_p,lat_p,
	                                 var,p):

	# Check time
	if time_p.size!=time_var.size:
		print 'Error: interpolate_on_p_profile_tlim'
		print 'pressure and variable do not have same number of time points'
		print 'time_p',time_p.size,'time_var',time_var.size
		sys.exit()
	elif (time_p!=time_var).any():
		print 'Error: interpolate_on_p_profile_tlim'
		print 'pressure and variable have same number of time points but grids do not match'
		#sys.exit()

	# Check longitude
	if lon_p.size!=lon_var.size:
		print 'Variable and pressure longitude grids do not have same number of points'	
		print 'variable points: ', lon_var.size, 'pressure points: ',lon_p.size 
		print 'interpolating variable onto pressure grid'
		var = interpolate_longitude(ntime,nheight,nlat,nlon,lon_p,lon_var,p,var)
	elif (lon_p!=lon_var).any():
		print 'Variable and pressure longitude grids have same number of points but do not match'
		print 'interpolating variable onto pressure grid'
		var = interpolate_longitude(ntime,nheight,nlat,nlon,lon_p,lon_var,p,var)
	# Check latitude
	if lat_p.size != lat_var.size:
		print 'Variable and pressure latitude grids do not have same number of points'	
		print 'variable points: ', lat_var.size, 'pressure points: ',lat_p.size 
		print 'interpolating variable onto pressure grid'
		var = interpolate_latitude(ntime,nheight,nlat,nlon,nlat_p,lat_p,lat_var,p,var)
	elif (lat_p!=lat_var).any():
		print 'Variable and pressure latitude grids have same number of points but do not match'
		print 'interpolating variable onto pressure grid'
		var = interpolate_latitude(ntime,nheight,nlat,nlon,lat_p,lat_var,p,var)
	return var
