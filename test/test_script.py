from um_post_proc import *
from pylab import *
import os
import shutil

# Set standard variables
fname = 'test_data/test_data.nc'
fname_keys = 'netcdf_keys'
save_dir = 'test_output/'

showfig=False
save_fig=True
read_saved_var = True
save_var = True
save_ext = '.pdf'

# Times
time = 1000.
time_1 = 990.
time_2 = 1000.


# Empty output directory
shutil.rmtree('test_output')
os.mkdir('test_output')

# ####################
# zonal tempoeral mean
# ####################

plot_um_2d(fname=fname,fname_keys=fname_keys,varname='u',plot_type='zonal_temporal_mean',
  time_1=time_1,time_2=time_2,
  cmap='bwr',cbar_type='symlog',cbar_label='$u$ [km/s]',
  contours=True,ncont=5,
  smooth=True,smooth_factor=2,
  showfig=showfig,save_fig=save_fig,read_saved_var=read_saved_var,save_ext=save_ext,save_var=save_var,save_dir=save_dir,
  fname_save='zonal_mean_zonal_wind')

clf()  
# ####################
# meridional tempoeral mean
# ####################
# Meridional mean vertical wind
plot_um_2d(fname=fname,fname_keys=fname_keys,varname='w',plot_type='meridional_temporal_mean',
  time_1=time_1,time_2=time_2,lat_min=-20.,lat_max=20.,
  cmap='bwr',cbar_type='midpoint',cbar_label='$w$ [km/s]',
  contours=True,ncont=5,
  smooth=True,smooth_factor=2,
  showfig=showfig,save_fig=save_fig,read_saved_var=read_saved_var,save_ext=save_ext,save_var=save_var,save_dir=save_dir,
  fname_save='merid_mean_vert_wind')

clf()
# ####################
# Latitude longitude 
# ####################


# Temperature on 1e4 Pa
plot_um_2d(fname=fname,fname_keys=fname_keys,varname='temp',plot_type='latitude_longitude',
  time_1=time_1,level=1e4,
  cmap='coolwarm',cbar_type='',cbar_label='Temperature [K]',
  contours=True,ncont=5,
  smooth=True,smooth_factor=2,
  wind_vectors=True,
  showfig=showfig,save_fig=save_fig,read_saved_var=read_saved_var,save_ext=save_ext,save_var=save_var,save_dir=save_dir,
  fname_save='temperature_p1e4')
  
clf()
  
# Surface Temperature
plot_um_2d(fname=fname,fname_keys=fname_keys,varname='surface_temp',plot_type='surface',
  time_1=time_1,level=1e4,
  cmap='coolwarm',cbar_type='',cbar_label='Temperature [K]',
  contours=True,ncont=5,
  smooth=True,smooth_factor=2,
  wind_vectors=True,
  showfig=showfig,save_fig=save_fig,read_saved_var=read_saved_var,save_ext=save_ext,save_var=save_var,save_dir=save_dir,
  fname_save='temperature_surface')

clf()


# ####################
# 1d profile
# ####################
lat = [0.]
lon = linspace(0.,360,15)

fig, ax = plt.subplots()

# Equilibrium
# CH4
plot_um_multi_1d(fname=fname,fname_keys=fname_keys,varname='ch4_mole_fraction',plot_type='column',
  time_1=1000,lon=lon,lat=lat,
  color='grey',linestyle='--',
  log_x=True,log_y=True,xlab='Mole Fraction',
  showfig=showfig,save_fig=True,save_var=save_var,read_saved_var=read_saved_var,save_ext=save_ext,save_dir=save_dir,
  fname_save='ch4_equator')
clf()
# Equilibrium
# CH4
plot_um_multi_1d(fname=fname,fname_keys=fname_keys,varname='ch4_mole_fraction',plot_type='column',
  time_1=1000,lon=lon,lat=lat,pressure_grid=False,
  color='grey',linestyle='--',
  log_x=True,log_y=False,xlab='Mole Fraction',
  showfig=showfig,save_fig=True,save_var=save_var,read_saved_var=read_saved_var,save_ext=save_ext,save_dir=save_dir,
  fname_save='ch4_equator_altitude')
clf()
#Dayside and nightside average temperature
plot_um_1d(fname=fname,fname_keys=fname_keys,varname='temp',plot_type='dayside_average_temporal_mean',
  time_1 = time_1, time_2=time_2,
  color='red',
  log_y=True,xlab='Temperature',
  showfig=showfig,save_fig=False,save_var=save_var,read_saved_var=read_saved_var,save_ext=save_ext,save_dir=save_dir,
  fname_save='temp_dayside')
plot_um_1d(fname=fname,fname_keys=fname_keys,varname='temp',plot_type='nightside_average',
  time_1 = 1000.,
  color='blue',
  log_y=True,xlab='Temperature',
  showfig=showfig,save_fig=True,save_var=save_var,read_saved_var=read_saved_var,save_ext=save_ext,save_dir=save_dir,
  fname_save='temp_nightside')

