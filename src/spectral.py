from constant_umpp import *
from read_variables import *
from interpolate_variable import *
from pylab import *
import sys
def process_spectral(t,z,lat,lon,band,var,fname,instrument):

  if verbose: 
    print 'process_spectral'
    print 'processing wavelength dimension'
    print 'for instrument: ',instrument

  # Read spectral file to get band limits
  wvmin, wvmax = read_spectral_wavelength(fname,band.size)

  # Get central wavelength of band
  wv = (wvmin+wvmax)*0.5

  var_new = zeros((t.size,z.size,lat.size,lon.size))
  # Sum over bands
  if instrument=='sum':
    for itime in range(t.size):
      for iheight in range(z.size):
        for ilat in range(lat.size):
          for ilon in range(lon.size):
            var_new[itime,iheight,ilat,ilon] = sum(var[itime,iheight,ilat,ilon,:])
  # Get in channel
  # Nearest band
  elif type(instrument) == float:
    index = argmin(abs(instrument-wv))
    var_new = var[:,:,:,:,index]
  else:
    channel_wv, response = read_instrument_response(instrument)
    for itime in range(t.size):
      for iheight in range(z.size):
        for ilat in range(lat.size):
          for ilon in range(lon.size):
            # interpolate to get variable on channel wavelengths
             var[itime,iheight,ilat,ilon,:] = var[itime,iheight,ilat,ilon,:]/(wvmax-wvmin)
             var_int = linear_interp_1d(wv,channel_wv,var[itime,iheight,ilat,ilon,:])
             var_new[itime,iheight,ilat,ilon] = sum(response*var_int)/sum(response)
            
  return var_new
 


def read_instrument_response(instrument):

        if instrument=='Spitzer3.6':
          fresponse='/data/bd257/observations/instrument_response/spitzer_irac/3.6channel.dat'
        elif instrument=='Spitzer4.5':
          fresponse='/data/bd257/observations/instrument_response/spitzer_irac/4.5channel.dat'
        elif instrument=='Spitzer5.8':
          fresponse='/data/bd257/observations/instrument_response/spitzer_irac/5.8channel.dat'
        elif instrument=='Spitzer8.0':
          fresponse='/data/bd257/observations/instrument_response/spitzer_irac/8.0channel.dat'
        else:
          print 'Error instrument not supported', instrument
          sys.exit()

        f = np.loadtxt(fresponse,skiprows=3)
        channel_wv = f[:,0]*1.0e-6 # convert to SI
        response   = f[:,1]

        return channel_wv, response
