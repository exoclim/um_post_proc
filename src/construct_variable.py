from read_variables import *
from interpolate_variable import *
from mean_variable import *
from pylab import *
from spectral import *

# Control function 2D plots
def construct_variable_2d(fname,fname_keys,fname_spec,varname,time_1,time_2,lon_request,lat_min,lat_max,level,plot_type,pressure_grid,vardim,instrument,nband):

  # Get which variable to read from netcdf file
  # varread = get_variable_to_read(varname)
  varread = read_netcdf_keys(fname_keys,varname)

  # Read variable
  if vardim == 4:
    t, z, lon, lat, var = read_variable_4d(fname,varread)
  else:
    t, z, lon, lat, band, var = read_variable_5d(fname,varread,nband)
    var = process_spectral(t,z,lat,lon,band,var,fname_spec,instrument)

  # Select which method to use to post process variable
  # Compute a zonal temporal mean
  if plot_type=='zonal_temporal_mean':
    x, y, var = zonal_temporal_mean(fname,varname,t,z,lat,lon,var,time_1,time_2,plot_type,pressure_grid)

  elif plot_type=='zonal_mean':
    x, y, var = zonal_mean(fname,varname,t,z,lat,lon,var,time_1,plot_type,pressure_grid)

  # Compute a meridional temporal mean
  elif plot_type=='meridional_temporal_mean':
    # Compute meridional temporal mean
    x, y, var = meridional_temporal_mean(fname,varname,t,z,lat,lon,var,time_1,time_2,lat_min,lat_max,plot_type,pressure_grid)

  # Compute a meridional mean at a snapshot
  elif plot_type=='meridional_mean':
    # Compute meridional mean
    x, y, var = meridional_mean(fname,varname,t,z,lat,lon,var,time_1,lat_min,lat_max,plot_type,pressure_grid)

  # Compute a latitude longitide snapshot
  elif plot_type=='latitude_longitude':
    # Compute pressure level
    x, y, var = latitude_longitude_slice(fname,varname,t,z,lat,lon,var,time_1,level,plot_type,pressure_grid)

  elif plot_type=='pressure_latitude':
    # Compute latitude slice at given longitude
    x, y, var = pressure_latitude(fname,varname,t,z,lat,lon,var,time_1,lon_request,plot_type)

  elif plot_type=='pressure_longitude':
    # Compute latitude slice at given longitude
    x, y, var = pressure_longitude(fname,varname,t,z,lat,lon,var,time_1,lat_min,plot_type)

  # Compute pressure time
  elif plot_type=='pressure_time':
    x, y, var = pressure_time(fname,varname,t,z,lat,lon,var,time_1,time_2,lat_min,lat_max,plot_type)

  elif plot_type=='latitude_time':
    x, y, var = latitude_time(fname,varname,t,z,lat,lon,var,time_1,time_2,level,lon_request,plot_type)

  # Surface variable (i.e. one vertical level)
  elif plot_type=='surface':
    x, y, var = surface(fname,varname,t,z,lat,lon,var,time_1,plot_type)

  # Surface variable temporal mean (i.e. one vertical level)
  elif plot_type=='surface_temporal_mean':
    x, y, var = surface_temporal_mean(fname,varname,t,z,lat,lon,var,time_1,time_2,plot_type)

  else:
    print 'Error: get_variable_2d'
    print '  plot_type',plot_type,'not implemented'
    sys.exit()

  return x, y, var

# Control function 1D plots	
def construct_variable_1d(fname,fname_keys,fname_spec,varname,time_1,time_2,lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid,vardim,instrument,nband):

	# Get which variable to read from netcdf file
	#varread = get_variable_to_read(varname)
	varread = read_netcdf_keys(fname_keys,varname)

        # Read variable (assumes it is a 4D variable)
        if vardim == 4:
          t, z, lon, lat, var = read_variable_4d(fname,varread)
        else:
          t, z, lon, lat, band, var = read_variable_5d(fname,varread,nband)
          var = process_spectral(t,z,lat,lon,band,var,fname_spec,instrument)


	# Select which method to use to post process variabl
	if plot_type=='area_average' or plot_type=='dayside_average' or plot_type=='nightside_average':
		y, var = area_average(fname,varname,t,z,lat,lon,var,time_1,lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid)
	elif plot_type=='dayside_average_temporal_mean' or plot_type=='nightside_average_temporal_mean':
		y, var = area_average_temporal_mean(fname,varname,t,z,lat,lon,var,time_1,time_2,lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid)
	elif plot_type=='column':
		y, var = extract_column(fname,varname,t,z,lat,lon,var,time_1,lat_min,lon_min,plot_type,pressure_grid)
	else:
		print 'Error: get_variable_1d'
		print '  plot_type',plot_type,'not implemented'
		sys.exit()
	
	return y, var
	
def construct_variable_multi_1d(fname,fname_keys,fname_spec,varname,time_1,time_2,lat_request,lon_request,plot_type,pressure_grid,vardim,instrument,nband):

	# Get which variable to read from netcdf file
	#varread = get_variable_to_read(varname)
	varread = read_netcdf_keys(fname_keys,varname)

        # Read variable (assumes it is a 4D variable)
        if vardim == 4:
          t, z, lon, lat, var = read_variable_4d(fname,varread)
        else:
          t, z, lon, lat, band, var = read_variable_5d(fname,varread,nband)
          var = process_spectral(t,z,lat,lon,band,var,fname_spec,instrument)

	# Select which method to use to post process variable
	if plot_type=='column':
		nlon, nlat, p, var = extract_column_multi(fname,varname,t,z,lat,lon,var,time_1,time_2,lat_request,lon_request,plot_type,pressure_grid)
	
	else:
		print 'Error: get_variable_multi_1d'
		print '  plot_type',plot_type,'not implemented'
		sys.exit()
		
	return nlon,nlat,p,var

# Create zonal temporal mean
def zonal_temporal_mean(fname,varname,time_var,height_var,lat_var,lon_var,var,time_1,time_2,plot_type,pressure_grid):
 
  # Interpolate variable onto uniform pressure grid between requested time limits
  if pressure_grid:
    vert_coord, lat, lon, var = interpolate_on_p_profile_time(time_var,height_var,lat_var,lon_var,var,time_1,time_2,fname)
  else:
    vert_coord = height_var
    lat = lat_var
    index =  array(where((time_var>=time_1) & (time_var<=time_2))).flatten()
    var = var[index,:,:,:]

  # Temporal mean  
  var = mean_var(var,axis=0)
 
  # Zonal mean
  var = mean_var(var,axis=2)
  
  # Post process variable
  #var = post_process_control(varname,var,vert_coord,plot_type)

  if verbose:
    print 'Constructed zonal temporal mean of variable:'
    print '  min value: ', amin(var), ' max value: ', amax(var)

  return lat, vert_coord, var
  
# Create zonal mean
def zonal_mean(fname,varname,time_var,height_var,lat_var,lon_var,var,time_1,plot_type,pressure_grid):
 
  # Interpolate variable onto uniform pressure grid between requested time limits
  if pressure_grid:  
    vert_coord, lat, lon, var = interpolate_on_p_profile(time_var,height_var,lat_var,lon_var,var,time_1,fname)
  else:
    vert_coord = height_var
    lat = lat_var
    index = argmin(abs(time_1-time_var))
    var = var[index,:,:,:]
 
  # Zonal mean
  var = mean_var(var,axis=2)
  
  # Post process variable
  #var = post_process_control(varname,var,vert_coord,plot_type)

  if verbose:
    print 'Constructed zonal temporal mean of variable:'
    print '  min value: ', amin(var), ' max value: ', amax(var)

  return lat, vert_coord, var

# Create meridional temporal mean
def meridional_temporal_mean(fname,varname,time_var,height_var,lat_var,lon_var,var,time_1,time_2,lat_min,lat_max,plot_type,pressure_grid):

  # Interpolate variable onto uniform pressure grid between requested time limits
  if pressure_grid:
    vert_coord, lat, lon, var = interpolate_on_p_profile_time(time_var,height_var,lat_var,lon_var,var,time_1,time_2,fname)
  else:
    vert_coord = height_var
    lon = lon_var
    index = array(where((time_var>=time_1) & (time_var<=time_2))).flatten()
    var = var[index,:,:,:]
  
  # Temporal mean
  var = mean_var(var,axis=0)
 
  # Meridional mean
  # Get indices of requested latitude limits
  index = array(where((lat>=lat_min) & (lat<=lat_max))).flatten()
  var = spatial_mean_weight_lim(lat,var[:,index,:],weights=cos(radians(lat[index])),axis=1)
  
  # Post process variable
  #var = post_process_control(varname,var,vert_coord,plot_type)

  if verbose:
    print 'Constructed meridional temporal mean of variable:'
    print '  min value: ', amin(var), ' max value: ', amax(var)

  return lon, vert_coord, var

# Create meridional temporal mean
def meridional_mean(fname,varname,time_var,height_var,lat_var,lon_var,var,time_1,lat_min,lat_max,plot_type,pressure_grid):

  # Interpolate variable onto uniform pressure grid between requested time limits
  if pressure_grid:
    vert_coord, lat, lon, var = interpolate_on_p_profile(time_var,height_var,lat_var,lon_var,var,time_1,fname)
  else:
    vert_coord = height_var
    lon = lon_var

    index = abs(argmin(time_1-time_var))
    var = var[index,:,:,:]
 
  # Meridional mean
  # Get indices of requested latitude limits
  index = array(where((lat_var>=lat_min) & (lat_var<=lat_max))).flatten()
  var = spatial_mean_weight_lim(lat_var,var[:,index,:],weights=cos(radians(lat_var[index])),axis=1)
  
  # Post process variable
  #var = post_process_control(varname,var,vert_coord,plot_type)

  if verbose:
    print 'Constructed meridional temporal mean of variable:'
    print '  min value: ', amin(var), ' max value: ', amax(var)

  return lon, vert_coord, var

# Create a latitude longitude slice
def latitude_longitude_slice(fname,varname,time_var,height_var,lat_var,lon_var,var,time_1,level,plot_type,pressure_grid):

  # Interpolate variable onto requested pressure point at requested time
  if pressure_grid:
    lat, lon, var_at_level = interpolate_on_p_point(time_var,height_var,lat_var,lon_var,var,time_1,level,fname)
    vert_coord = level
  else:
    lat = lat_var 
    lon = lon_var
    vert_coord = height_var
    # Get variable at requested time
    index = argmin(abs(time_var-time_1))
    var = var[index,:,:,:]
    
    # Get variable on requested altitude point 
    var_at_level = np.zeros((lat_var.size,lon_var.size))
    for ilat in range(lat_var.size):
      for ilon in range(lon_var.size):
        var_at_level[ilat,ilon] = linear_interp_1d(height_var,level,var[:,ilat,ilon])

  # Post process variable
  #var = post_process_control(varname,var_at_level,vert_coord,plot_type)
  var = var_at_level

  if verbose:
    print 'Constructed pressure slice of variable ', varname,' min value: ', amin(var), ' max value: ', amax(var)

  return lon, lat, var

def pressure_latitude(fname,varname,time_var,height_var,lat_var,lon_var,var,time_1,lon_request,plot_type):

  # Interpolate variable onto presure grid
  p, lat, lon, var = interpolate_on_p_profile(time_var,height_var,lat_var,lon_var,var,time_1,fname)
  
  # Get variable near requested longitude
  index = argmin(abs(lon-lon_request))
  var = var[:,:,index]
  
  # Post process variable
  #var = post_process_control(varname,var,p,plot_type)

  return lat, p, var
  
def pressure_longitude(fname,varname,time_var,height_var,lat_var,lon_var,var,time_1,lat_request,plot_type):

  # Interpolate variable onto presure grid
  p, lat, lon, var = interpolate_on_p_profile(time_var,height_var,lat_var,lon_var,var,time_1,fname)
  
  # Get variable near requested longitude
  index = argmin(abs(lat-lat_request))
  var = var[:,index,:]
  
  # Post process variable
  #var = post_process_control(varname,var,p,plot_type)

  return lon, p, var
      

def pressure_time(fname,varname,time_var,height_var,lat_var,lon_var,var,time_1,time_2,lat_min,lat_max,plot_type):

  if verbose:
    print 'Calculating variable as a function of pressure and time:'
    print '  time_min: ', time_1
    print '  time_max: ', time_2
    print '  lat_min:  ', lat_min
    print '  lat_max:  ', lat_max

  # Interpolate in P grid 
  p, lat, lon, var = interpolate_on_p_profile_time(time_var,height_var,lat_var,lon_var,var,time_1,time_2,fname)

  # Compute meridional mean
  index = array(where((lat_var>=lat_min) & (lat_var<=lat_max))).flatten()
  var = spatial_mean_weight_lim(lat_var,var[:,:,index,:],weights=cos(radians(lat_var[index])),axis=2)
  
  # Compute zonal mean
  var = mean_var(var,axis=2)
  
  if verbose:
    print 'Constructed variable ', varname,' min value: ', amin(var), ' max value: ', amax(var)
  
  return time_var, p, var.T
  
def latitude_time(fname,varname,time_var,height_var,lat_var,lon_var,var,time_1,time_2,level,lon_request,plot_type):

  if verbose:
    print 'Calculating variable as a function of pressure and time:'
    print '  time_min: ', time_1
    print '  time_max: ', time_2

  # Interpolate onto P point at requested time
  lat , lon, var = interpolate_on_p_point_time(time_var,height_var,lat_var,lon_var,var,level,fname)
  
  # Interpolate to get variable at requested longitude
  var_interp = zeros((time_var.size,lat_var.size))
  for itime in range(time_var.size):
    for ilat in range(lat_var.size):
      var_interp[itime,ilat] = linear_interp_1d(lon_var,lon_request,var[itime,ilat,:])
  
  var = var_interp
  
  return time_var, lat, var.T

# Get variable defined at surface
def surface(fname,varname,time_var,height_var,lat_var,lon_var,var,time_1,plot_type):

  # Get variable at requested time
  itime = argmin(abs(time_1-time_var))
  
  var = var[itime,0,:,:]

  if verbose:
    print 'Calculating surface variable'
    print ' time: ',time_var[itime]
  
  #pdummy = 1.0 # Not read in pressure, pass dummy argument 
  # Post process
  #var = post_process_control(varname,var,pdummy,plot_type)
  
  return lon_var,lat_var, var
  
# Get variable defined at surface
def surface_temporal_mean(fname,varname,time_var,height_var,lat_var,lon_var,var,time_1,time_2,plot_type):

  # Interpolate to get variable at requested time
  itime_1 = argmin(abs(time_var-time_1))
  itime_2 = argmin(abs(time_var-time_2))
  
  var = mean_var(var[itime_1:itime_2,0,:,:],axis=0)

  if verbose:
    print 'Calculating surface variable'
    print ' temporal mean: ',time_var[itime_1],time_var[itime_2]
  
  ##pdummy = 1.0 # Not read in pressure, pass dummy argument 
  # Post process
  #var = post_process_control(varname,var,pdummy,plot_type)
  
  return lon_var,lat_var, var

# Create single column profile
def extract_column(fname,varname,t,z,lat,lon,var,time_min,lat_request,lon_request,plot_type,pressure_grid):
#fname,varname,lon_request,lat_request,time_min,time_max,plot_type):

  if verbose:
    print 'Getting time averaged variable at specific latitude/longitude point'
    print '  longitude: ',lon_request
    print '  latitude:  ',lat_request

  # Interpolate in P grid 
  if pressure_grid:
    vert_coord, lat, lon, var = interpolate_on_p_profile(t,z,lat,lon,var,time_min,fname)
  else:
    vert_coord = height_var
    
  # Interpolate to get profile at requested points
  var_at_point = interpolate_latitude_longitude_2d(vert_coord,lon,lat,lon_request,lat_request,var)
  
  # Post process variable
  #var = post_process_control(varname,var_at_point,vert_coord,plot_type)
  var = var_at_point
  
  return vert_coord, var

# Hemisphere average
def area_average(fname,varname,time_var,height_var,lat_var,lon_var,var,time,lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid):

	if verbose:
		print 'Getting spatial temporal average'
		print '  time: ',time
		if plot_type=='dayside_average':
			print 'dayside average'
		elif plot_type=='nightside_average':
			print 'nightside average'
		else:
			print '  lat_min:  ', lat_min
			print '  lat_max:  ', lat_max
			print '  lon_min:  ', lon_min
			print ' lon_max:   ', lon_max

	# Interpolate in P grid 
	if pressure_grid:  
		vert_coord, lat, lon, var = interpolate_on_p_profile(time_var,height_var,lat_var,lon_var,var,time,fname)
	else:
		vert_coord = height_var

	if plot_type=='dayside_average':
		coslon = cos(radians(lon_var))
		coslat = cos(radians(lat_var))
		index_lon = array(where((coslon<0.))).flatten()
		index_lat = array(where((coslat>0.))).flatten()
	elif plot_type=='nightside_average':
		coslon = cos(radians(lon_var))
		coslat = cos(radians(lat_var))
		index_lon = array(where((coslon>0.))).flatten()
		index_lat = array(where((coslat>0.))).flatten()
	else:
		index_lon = array(where((lon>=lon_min) & (lon<=lon_max))).flatten()
		index_lat = array(where((lat>=lat_min) & (lat<=lat_max))).flatten()

	# Compute latitude mean
	var = spatial_mean_weight_lim(lat,var[:,index_lat,:],weights=cos(radians(lat[index_lat])),axis=1)

	# Compute longitude mean
	var = mean(var[:,index_lon],axis=1)

	# Post process variable
	#var = post_process_control(varname,var,vert_coord,plot_type)

	return vert_coord, var

# Hemisphere average
def area_average_temporal_mean(fname,varname,time_var,height_var,lat_var,lon_var,var,time_1,time_2,lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid):

	# Get indices for temporal mean
	itime_1 = argmin(abs(time_var-time_1))
	itime_2 = argmin(abs(time_var-time_2))

	if verbose:
		print 'Getting spatial temporal average'
		print '  temporal mean: ',time_var[itime_1],time_var[itime_2]
		if plot_type=='dayside_average':
			print 'dayside average'
		elif plot_type=='nightside_average':
			print 'nightside average'
		else:
			print '  lat_min:  ', lat_min
			print '  lat_max:  ', lat_max
			print '  lon_min:  ', lon_min
			print ' lon_max:   ', lon_max

	# Interpolate in P grid 
	if pressure_grid:  
		vert_coord, lat, lon, var = interpolate_on_p_profile_time(time_var,height_var,lat_var,lon_var,var,time_1,time_2,fname)
	else:
		vert_coord = height_var

	if plot_type=='dayside_average_temporal_mean':
		coslon = cos(radians(lon_var))
		coslat = cos(radians(lat_var))
		index_lon = array(where((coslon<0.))).flatten()
		index_lat = array(where((coslat>0.))).flatten()
	elif plot_type=='nightside_average_temporal_mean':
		coslon = cos(radians(lon_var))
		coslat = cos(radians(lat_var))
		index_lon = array(where((coslon>0.))).flatten()
		index_lat = array(where((coslat>0.))).flatten()
	else:
		index_lon = array(where((lon>=lon_min) & (lon<=lon_max))).flatten()
		index_lat = array(where((lat>=lat_min) & (lat<=lat_max))).flatten()

	# Compute temporal mean
	var = mean_var(var,axis=0)

	# Compute latitude mean
	var = spatial_mean_weight_lim(lat,var[:,index_lat,:],weights=cos(radians(lat[index_lat])),axis=1)

	# Compute longitude mean
	var = mean(var[:,index_lon],axis=1)

	# Post process variable
	#var = post_process_control(varname,var,vert_coord,plot_type)

	return vert_coord, var

# Create multiple columns
def extract_column_multi(fname,varname,time_var,height_var,lat_var,lon_var,var,time_1,time_2,lat_request,lon_request,plot_type,pressure_grid):

  if verbose:
    print 'Getting time averaged variable at requested latitude/longitude points'
    print '  longitudes: ',lon_request
    print '  latitudes: ', lat_request

  # Get number of latitudes and number of longitudes
  nlon = len(lon_request)
  nlat = len(lat_request)

  # Interpolate onto P grid
  if pressure_grid:
    vert_coord, lat, lon, var = interpolate_on_p_profile(time_var,height_var,lat_var,lon_var,var,time_1,fname)
  else:
    vert_coord = height_var
    index = argmin(abs(time_var-time_1))
    var = var[index,:,:,:]
    
  # Interpolate to get profile at requested points
  var_at_point = zeros((vert_coord.size,nlat,nlon))
  for ilat in range(nlat):
    for ilon in range(nlon):
      var_at_point[:,ilat,ilon] = interpolate_latitude_longitude_2d(vert_coord,lon_var,lat_var,lon_request[ilon],lat_request[ilat],var)
      
  # Post process variable
  #var = post_process_control(varname,var_at_point,vert_coord,plot_type)
  var = var_at_point

  return nlat, nlon, vert_coord, var

