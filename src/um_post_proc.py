from construct_variable import *
from calculate_variable import *
from save_var import *
from pylab import *
from matplotlib.mlab import bivariate_normal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import os

# Function to read or calculate requested 2d variable
def get_variable_2d(save_dir,fname,fname_keys,fname_spec,fname_save,varname,read_saved_var,save_var,time_1,time_2,lon,lat_min,lat_max,plevel,plot_type,pressure_grid,vardim,instrument,nband):

	# Read variable from saved file
	if read_saved_var and os.path.isfile(save_dir+'saved_vars/'+fname_save+'_'+varname):
		y, x, var = read_saved_var_2d(save_dir,fname_save+'_'+varname)

	else:
		
		# Construct variable
		x, y, var = calculate_variable(fname,fname_keys,fname_spec,varname,time_1,time_2,lon,lat_min,lat_max,plevel,plot_type,pressure_grid,vardim,instrument,nband)
		
		# Save variable
		if save_var:
			save_var_2d(save_dir,fname_save+'_'+varname,x,y,var)

	return x, y, var
	
# Function to read and/or calculate requested 1d variable
def get_variable_1d(save_dir,fname,fname_keys,fname_spec,fname_save,varname,read_saved_var,save_var,time_1,time_2,lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid,vardim,instrument,nband):
	
	# Read variable from saved file
	if read_saved_var and os.path.isfile(save_dir+fname_save):
		y, var = read_saved_var_1d(save_dir,fname_save)
		
	else:
	  y, var = construct_variable_1d(fname,fname_keys,fname_spec,varname,time_1,time_2,lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid,vardim,instrument,nband)
	  
	  # Save
	  if save_var:
	    save_var_1d(save_dir,fname_save,y,var)
	 
	return y, var
	
def get_variable_multi_1d(save_dir,fname,fname_keys,fname_spec,fname_save,varname,read_saved_var,save_var,time_1,time_2,lat,lon,plot_type,pressure_grid,vardim,instrument,nband):
	
	# Read variable from saved file
	if read_saved_var and os.path.isfile(save_dir+fname_save):
		p, lat, lon, var = read_saved_var_3d(save_dir,fname_save)
		nlat = lat.size
		nlon = lon.size
	else:
		# Construct variable
		nlon, nlat, y, var = construct_variable_multi_1d(fname,fname_keys,fname_spec,varname,time_1,time_2,lat,lon,plot_type,pressure_grid,vardim,instrument,nband)

		# Save
		if save_var:
			save_var_3d(save_dir,fname_save,y,asarray(lat),asarray(lon),var)
	
	return nlat, nlon, y, var

def get_wind_vectors(save_dir,fname,fname_keys,fname_spec,fname_save,varname,read_saved_var,save_var,time_1,time_2,lon,lat_min,lat_max,plevel,plot_type,pressure_grid,vardim,instrument,nband):

  # Read wind vectors
  if plot_type=='latitude_longitude' or plot_type=='surface':
    x1, y1, u = get_variable_2d(save_dir,fname,fname_keys,fname_spec,fname_save,'u',read_saved_var,save_var,time_1,time_2,lon,lat_min,lat_max,plevel,'latitude_longitude',pressure_grid,vardim,instrument,nband)
    x2, y2, v = get_variable_2d(save_dir,fname,fname_keys,fname_spec,fname_save,'v',read_saved_var,save_var,time_1,time_2,lon,lat_min,lat_max,plevel,'latitude_longitude',pressure_grid,vardim,instrument,nband)
    ynew = linspace(amin(y1),amax(y1),12)

  elif plot_type=='meridional_mean' or plot_type=='meridional_temporal_mean':
    x1, y1, u = get_variable_2d(save_dir,fname,fname_keys,fname_spec,fname_save,'u',read_saved_var,save_var,time_1,time_2,lon,lat_min,lat_max,plevel,plot_type,pressure_grid,vardim,instrument,nband)
    x2, y2, v = get_variable_2d(save_dir,fname,fname_keys,fname_spec,fname_save,'w',read_saved_var,save_var,time_1,time_2,lon,lat_min,lat_max,plevel,plot_type,pressure_grid,vardim,instrument,nband)  
    ynew = logspace(amin(log10(y1)),amax(log10(y1)),12)
  elif plot_type=='pressure_latitude':
    x1, y1, u = get_variable_2d(save_dir,fname,fname_keys,fname_spec,fname_save,'v',read_saved_var,save_var,time_1,time_2,lon,lat_min,lat_max,plevel,plot_type,pressure_grid,vardim,instrument,nband)
    x2, y2, v = get_variable_2d(save_dir,fname,fname_keys,fname_spec,fname_save,'w',read_saved_var,save_var,time_1,time_2,lon,lat_min,lat_max,plevel,plot_type,pressure_grid,vardim,instrument,nband)  
    ynew = logspace(amin(log10(y1)),amax(log10(y1)),12)

  else:
    print 'Error: get_wind_vectors'
    print 'wind vectors not supported for plot_type',plot_type
    sys.exit()
    
  # Interpolate
  print ynew
  xnew = linspace(amin(x1),amax(x2),12)
  u = linear_interp_2d(x1,xnew,y1,ynew,u)
  v = linear_interp_2d(x2,xnew,y2,ynew,v)
  
  return xnew,ynew,u, v
  
# Function to create a 2D plot 
def plot_um_2d(fname,fname_keys,varname,plot_type,
# Optional variables
varname2=None,
vardim=4,
fname_spec='',
instrument=None,
nband=None,
# Dimension variables
time_1=None,time_2=None,level=None,lat_min=None,lat_max=None,lon=None,
pressure_grid=True,
# Plotting variables
vmin=None,vmax=None,color_map=True,cmap='Blues',smooth=False,smooth_log=False,smooth_factor=1,cbar_label='',cbar_type='',
# Contour variables
contours=False,ncont=5,cont_scale='linear',cont_colour=['black'],cont_linewidth=[1],cont_min=None,cont_max=None,
# Wind vectors
wind_vectors=False,
# Plot parameters
ymin=None,ymax=None,
# Parameters
showfig=False,save_fig=False,fname_save='um_post_proc',plot_title=None,read_saved_var=False,save_var=False,save_dir='',save_ext='.png'):


  # Get variable
  x, y, var = get_variable_2d(save_dir,fname,fname_keys,fname_spec,fname_save,varname,read_saved_var,save_var,time_1,time_2,lon,lat_min,lat_max,level,plot_type,pressure_grid,vardim,instrument,nband)
  
  # If taking ratio with second variable
  if varname2!=None:
    x2, y2, var2 = get_variable_2d(save_dir,fname,fname_keys,fname_save,varname2,read_saved_var,save_var,time_1,time_2,lon,lat_min,lat_max,level,plot_type,pressure_grid,vardim,instrument,nband)
    var = var/var2

  # Plot
  plot_variable_2d(y,x,var,plot_type,smooth,smooth_factor,smooth_log,vmin,vmax,cont_min,cont_max,
  color_map,cmap,cbar_label,cbar_type,contours,ncont,cont_scale,cont_colour,cont_linewidth,
  ymin,ymax,pressure_grid)
  
  if wind_vectors:
    # Plot wind vectors
    xwind,ywind,wind1, wind2 = get_wind_vectors(save_dir,fname,fname_keys,fname_spec,fname_save,varname,read_saved_var,save_var,time_1,time_2,lon,lat_min,lat_max,level,plot_type,pressure_grid,vardim,instrument,nband)
      
    quiver(xwind,ywind,wind1,wind2,color='black')
  
  if plot_title!=None:
    title(plot_title,fontsize=20)
  
  # Save figure as pdf
  if save_fig:
    savefig(save_dir+fname_save+save_ext)
    if verbose:
      print 'Saved figure at: ',save_dir+fname_save+'.pdf'
  
  # Show figure on screen
  if showfig:
    show()
    
# Function to create a 2D difference plot 
def plot_um_2d_diff(fname_1,fname_2,fname_keys,varname,plot_type,
# Dimension variables
time_min_1=None,time_min_2=None,time_max_1=None,time_max_2=None,level=None,lat_min=None,lat_max=None,lon=None,
pressure_grid=True,
log_var=False,
vardim=4,
fname_spec='',
instrument=None,
nband=None,
# Plotting variables
vmin=None,vmax=None,color_map=True,cmap='Blues',smooth=False,smooth_log=False,smooth_factor=1,cbar_label='',cbar_type='',
# Contour variables
contours=False,ncont=5,cont_scale='linear',cont_colour=['black'],cont_linewidth=[1],cont_min=None,cont_max=None,
# Plot parameters
ymin=None,ymax=None,
# Parameters
rel_diff=False,showfig=False,save_fig=False,fname_save='um_post_proc',plot_title='',read_saved_var=False,save_var=False,save_dir='',save_ext='.png'):

  # Get variable 1
  x1, y1, var1 = get_variable_2d(save_dir,fname_1,fname_keys,fname_spec,fname_save+'1',varname,read_saved_var,save_var,time_min_1,time_max_1,lon,lat_min,lat_max,level,plot_type,pressure_grid,vardim,instrument,nband)
  # Get variable 2
  x2, y2, var2 = get_variable_2d(save_dir,fname_2,fname_keys,fname_spec,fname_save+'2',varname,read_saved_var,save_var,time_min_2,time_max_2,lon,lat_min,lat_max,level,plot_type,pressure_grid,vardim,instrument,nband)
 
  if log_var:
    var1 = log10(var1)
    var2 = log10(var2)
 
  # Check that variables are on same grid
  if (y1 != y2).any():
    print 'Warning: plot_um_2d_diff'
    print '  y dimensions of variables do not match'
    print 'y1: ', y1
    print 'y2: ', y2
  elif (x1!= x2).any():
    print 'Error: plot_um_2d_diff'
    print ' x dimensions of variables do not match'
    print 'x1: ', x1
    print 'x2: ', x2
    sys.exit()
  else:
    x = x1
    y = y1
  
  x = x1
  y = y1
  # Take difference
  if verbose:
    print 'Taking difference between variables'
  if rel_diff:
    var = var2-var1
    var = var/var2
    if verbose:
      print 'relative difference, max: ', amax(var), 'min: ',amin(var)
  else:
    var = var2-var1
    if verbose:
      print 'absolute difference, max: ', amax(var), 'min: ',amin(var)
  
  # Plot
  plot_variable_2d(y,x,var,plot_type,smooth,smooth_factor,smooth_log,vmin,vmax,cont_min,cont_max,
  color_map,cmap,cbar_label,cbar_type,contours,ncont,cont_scale,cont_colour,cont_linewidth,
  ymin,ymax,pressure_grid)
  
  # Save figure as pdf
  if save_fig:
    savefig(save_dir+fname_save+save_ext)
    if verbose:
      print 'Saved figure at: ',save_dir+fname_save+'.pdf'
  
  # Show figure on screen
  if showfig:
    show()

# Function to plot 2d variable
def plot_variable_2d(y,x,var,plot_type,smooth,smooth_factor,smooth_log,vmin,vmax,cont_min,cont_max,
color_map,cmap,cbar_label,cbar_type,contours,ncont,cont_scale,cont_colour,cont_linewidth,ymin,ymax,pressure_grid):

	# Smoothing
	if smooth:
		if plot_type=='zonal_temporal_mean' or plot_type=='zonal_mean' or plot_type=='meridional_temporal_mean' or plot_type=='meridional_mean' or plot_type=='pressure_latitude' or plot_type=='pressure_longitude':
			x, y, var = smooth_2d_xlinear_ylog(x,y,var,smooth_factor,smooth_log)
		else:
			x, y, var = smooth_2d(x,y,var,smooth_factor,smooth_log)

	# Check limits of plot
	if vmin == None:
		vmin = amin(var)
	if vmax == None:
		vmax = amax(var)
	if cont_min == None:
		cont_min = amin(var)
	if cont_max == None:
		cont_max = amax(var)

	# Plot
	if color_map:
	  plot_2d(x,y,var,cmap,vmin,vmax,cbar_label,cbar_type)

	# Add contours
	if contours:
		plot_contour(x,y,var,cont_min,cont_max,ncont,cont_scale,cont_colour,cont_linewidth)

	# Set yaxis
	if plot_type=='zonal_temporal_mean' or plot_type=='zonal_mean' or plot_type=='meridional_temporal_mean' or plot_type=='meridional_mean' or plot_type=='pressure_time' or plot_type=='pressure_latitude' or plot_type=='pressure_longitude':
		if pressure_grid:
                  yscale('log')
                  ylim(amax(y),amin(y))
		  ylabel('Pressure [Pa]',fontsize=20)
		else:
                  ylim(amin(y),amax(y))
		  ylabel('Altitude',fontsize=20)
	else:
		ylim(amin(y),amax(y))
		ylabel('Latitude [deg]',fontsize=20)
		ax = gca()
		majorLocator = FixedLocator([-60.,-30.,0.,30.,60.])
		ax.yaxis.set_major_locator(majorLocator)
		ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
		
	# Overide ylimit
	if ymin!=None and ymax!=None:
	  ylim(ymin,ymax)
	elif ymin!=None:
	  ylim(ymin,amax(y))
	elif ymax!=None:
	  ylim(amin(y),ymax)

	# Set x axis
	xlim(amin(x),amax(x))
	if plot_type=='zonal_temporal_mean' or plot_type=='zonal_mean' or plot_type=='pressure_latitude':
		xlabel('Latitude [deg]',fontsize=20)
		ax = gca()
		majorLocator = FixedLocator([-60.,-30.,0.,30.,60.])
		ax.xaxis.set_major_locator(majorLocator)
		ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
	elif plot_type=='latitude_longitude' or plot_type=='meridional_temporal_mean' or plot_type=='meridional_mean' or plot_type=='pressure_longitude':
		xlabel('Longitude [deg]',fontsize=20)
		ax = gca()
		majorLocator = FixedLocator([0.,45.,90.,135.,180.,225.,270.,315.,360.])
		ax.xaxis.set_major_locator(majorLocator)
		ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
	elif plot_type=='pressure_time' or plot_type=='latitude_time':	
		xlabel('Time [days]',fontsize=20)

def plot_variable_1d(y,var,color,alpha,linewidth,linestyle,label,log_x,log_y,xmin,xmax,ymin,ymax,xlab,pressure_grid):  

  # Check limits of plot
	if xmin == None:
		xmin = amin(var)
	if xmax == None:
		xmax = amax(var)
	if ymin == None:
		ymin = amin(y)
	if ymax == None:
		ymax = amax(y)  # assume pressure

	# Plot
	plot_1d(var,y,color,alpha,linestyle,linewidth,label,log_y)
	
	# Set axes - assume pressure for y axis
	ylim(ymax,ymin)
	if pressure_grid:
	
	  ylabel('Pressure [Pa]',fontsize=20)
	else:
	  ylabel('Altitude',fontsize=20)
	if log_y:
	  yscale('log')
	
	xlim(xmin,xmax)
	xlabel(xlab,fontsize=20)
	if log_x:
	  xscale('log')

def plot_um_1d(fname,varname,plot_type,fname_keys,
# Dimension variables
time_1=None,time_2=None,lat_min=None,lat_max=None,lon_min=None,lon_max=None,
pressure_grid=True,
vardim=4,
fname_spec='',
nband=None,
instrument=None,
# Plotting variables
color='black',alpha=1.,linewidth=2,linestyle='-',label='',log_x=False,log_y=False,xmin=None,xmax=None,ymin=None,ymax=None,xlab='',
# Parameters
showfig=False,save_fig=False,fname_save='um_post_proc',plot_title='',read_saved_var=False,save_var=False,save_dir='',save_ext='.png'):

  # Get variable
  y, var = get_variable_1d(save_dir,fname,fname_keys,fname_spec,fname_save,varname,read_saved_var,save_var,time_1,time_2,lat_min,lat_max,lon_min,lon_max,plot_type,pressure_grid,vardim,instrument,nband)

  # Plot
  plot_variable_1d(y,var,
  color,alpha,linewidth,linestyle,label,log_x,log_y,xmin,xmax,ymin,ymax,xlab,pressure_grid)
  
  # Save figure as pdf
  if save_fig:
    savefig(save_dir+fname_save+save_ext)
    if verbose:
      print 'Saved figure at: ',save_dir+fname_save+'.pdf'
  
  # Show figure on screen
  if showfig:
    show()

def plot_um_multi_1d(fname,fname_keys,varname,plot_type,
# Dimension variables
time_1=None,time_2=None,lon=None,lat=None,
pressure_grid=True,
vardim=4,
fname_spec=None,
instrument=None,
# Plotting variables
color='black',alpha=1.,linewidth=1,linestyle='-',label='',log_x=False,log_y=False,xmin=None,xmax=None,ymin=None,ymax=None,xlab='',
# Parameters
showfig=False,save_fig=False,fname_save='um_post_proc',plot_title='',read_saved_var=False,save_var=False,save_dir='',save_ext='.png'):

  # Get variable
  nlon, nlat, y, var = get_variable_multi_1d(save_dir,fname,fname_keys,fname_spec,fname_save,varname,read_saved_var,save_var,time_1,time_2,lat,lon,plot_type,pressure_grid,vardim,instrument)

  # Plot
  for ilat in range(nlat):
    for ilon in range(nlon):
      plot_variable_1d(y,var[:,ilat,ilon],
      color,alpha,linewidth,linestyle,label,log_x,log_y,xmin,xmax,ymin,ymax,xlab,pressure_grid)
      
  
  # Save figure as pdf
  if save_fig:
    savefig(save_dir+fname_save+save_ext)
    if verbose:
      print 'Saved figure at: ',save_dir+fname_save+'.pdf'
  
  # Show figure on screen
  if showfig:
    show()
    
def plot_1d(x,y,color,alpha,linestyle,linewidth,label,log_y):

  if verbose:
    print 'Plotting variable'

  # Plot
  plot(x,y,color=color,linestyle=linestyle,linewidth=linewidth,label=label,alpha=alpha)

  if log_y:
    yscale('log')

def plot_2d(x,y,z,cmap,vmin,vmax,cbar_label,plot_type):

  if verbose:
    print 'Plotting variable'
    
  # Plot 
  if plot_type=='midpoint':
    pcm = pcolormesh(x,y,z,cmap=cmap,norm=MidpointNormalize(midpoint=0.),vmin=vmin,vmax=vmax,linewidth=0,rasterized=True)
  elif plot_type=='midpoint_1':
    pcm = pcolormesh(x,y,z,cmap=cmap,norm=MidpointNormalize(midpoint=1.),vmin=vmin,vmax=vmax,linewidth=0,rasterized=True)
  elif plot_type=='log':
    pcm = pcolormesh(x,y,z,cmap=cmap,norm=colors.LogNorm(vmin=z.min(), vmax=z.max()),vmin=vmin,vmax=vmax,linewidth=0,rasterized=True)
  elif plot_type=='symlog':
    pcm = pcolormesh(x,y,z,cmap=cmap,norm=colors.SymLogNorm(linthresh=0.06,linscale=0.3,vmin=z.min(), vmax=z.max()),vmin=vmin,vmax=vmax,linewidth=0,rasterized=True)
  else:
    pcm = pcolormesh(x,y,z,cmap=cmap,vmin=vmin,vmax=vmax,linewidth=0,rasterized=True)

  # Add colorbar
  cb = colorbar(pcm,extend='both')
  cb.set_label(cbar_label,fontsize=20)

def plot_contour(x,y,z,cont_min,cont_max,ncont,scale,color,linewidth):

  if verbose:
    print 'Plotting contours' 

  # Contour levels
  if scale == 'linear':
    dcon = (cont_max-cont_min)/ncont
    con_levels = linspace(cont_min+dcon,cont_max-dcon,ncont)
    cont_fmt = '%1.1f'
  elif scale == 'linear_log_label':
    dcon = (cont_max-cont_min)/ncont
    con_levels = linspace(cont_min+dcon,cont_max-dcon,ncont)
    cont_fmt = '%1.1e'    
  elif scale == 'log':
    dcon = (log10(cont_max)-log10(cont_min))/ncont
    con_levels = logspace(log10(cont_min)+dcon,log10(cont_max)-dcon,ncont)
    cont_fmt = '%1.1e'

  if verbose:
    print '  contour levels: ', con_levels
 
  # Plot contours
  cr = contour(x,y,z,con_levels,colors=color,linewidths=linewidth)

  # Plot contour labels
  clabel(cr,inline=True,fmt=cont_fmt,fontsize=12,use_clabeltext=True,)

# Function to smooth 2d data with logarithm 
def smooth_2d_xlinear_ylog(x,y,z,smooth_factor,smooth_log):

	if verbose:
		print 'Performing smoothing by cubic interpolation, smoothing factor:', smooth_factor
		print ' smoothing with x dimension linear, y dimension logarithmic'

	# Perform interpolation in log space
	if smooth_log:
		z = log10(z)

	# Define new dimensions
	xnew = linspace(amin(x),amax(x),int(x.size*smooth_factor))
	ynew = logspace(amin(log10(y)),amax(log10(y)),int(y.size*smooth_factor))

	# Interpolate
	znew = cubic_interp_2d(x,xnew,y,ynew,z)

	if smooth_log:
		znew = 10.**znew
	
	if verbose: 
		print 'variable smoothed'
		print '  new variable max:', amax(znew), 'min: ', amin(znew)

	return xnew, ynew,znew

def smooth_2d(x,y,z,smooth_factor,smooth_log):

  if verbose:
    print 'Performing smoothing by cubic interpolation, smoothing factor:', smooth_factor

  # Perform interpolation in log space
  if smooth_log:
    z = log10(z)
  
  # Define new dimensions
  xnew = linspace(amin(x),amax(x),int(x.size*smooth_factor))
  ynew = linspace(amin(y),amax(y),int(y.size*smooth_factor))

  # Interpolate
  znew = cubic_interp_2d(x,xnew,y,ynew,z)

  if smooth_log:
    znew = 10.**znew
    
  if verbose: 
    print 'variable smoothed'
    print '  new variable max:', amax(znew), 'min: ', amin(znew)

  return xnew, ynew,znew

class MidpointNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))


