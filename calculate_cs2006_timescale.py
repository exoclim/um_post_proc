from pylab import *

# Script to Compute the CO-CH4 chemical timescale and dynamical timescale

h2coeff = [3.10501126E+00,3.87207292E-04,3.65811209E-07,-2.74517202E-10,6.56030779E-14,-8.99596963E+02,-2.09912576E+00,
2.46899055E+00,6.53957408E-03,-1.47074304E-05,1.42487390E-08,-4.90075762E-12,-9.22698236E+02,1.10509172E-01]

cocoeff = [ 3.02507800E+00,1.44268850E-03,-5.63082700E-07,1.01858130E-10,-6.91095100E-15,-1.42683500E+04,6.10821700E+00,
3.26245100E+00,1.51194090E-03,-3.88175500E-06,5.58194400E-09,-2.47495100E-12,-1.43105390E+04,4.84889700E+00]

ch3ocoeff = [ 6.45804000E+00,3.22182000E-03,-5.09801000E-07,4.41966000E-11,-1.69366000E-15,-8.23233000E+02,-1.22475000E+01,
2.40571000E-01,1.87747000E-02,-2.13180000E-05,1.81151000E-08,-6.61230000E-12,1.35827000E+03,2.11815000E+01]

P0 = 1.013250e+5 
xh2 = 0.853
kb = 1.380620E-23

def compute_timescale(p,t):

	timescale = np.zeros(t.size)

	for i in range(t.size):
	
		if t[i] > 1000.:
			muh2 = h2coeff[0]*(1.-log(t[i])) - h2coeff[1]*t[i]/2. - h2coeff[2]*t[i]**2./6. - h2coeff[3]*t[i]**3./12. - h2coeff[4]*t[i]**4./20. + h2coeff[5]/t[i] - h2coeff[6]
			muco = cocoeff[0]*(1.-log(t[i])) - cocoeff[1]*t[i]/2. - cocoeff[2]*t[i]**2./6. - cocoeff[3]*t[i]**3./12. - cocoeff[4]*t[i]**4./20. + cocoeff[5]/t[i] - cocoeff[6]
			much3o = ch3ocoeff[0]*(1.-log(t[i])) - ch3ocoeff[1]*t[i]/2. - ch3ocoeff[2]*t[i]**2./6. - ch3ocoeff[3]*t[i]**3./12. - ch3ocoeff[4]*t[i]**4./20. + ch3ocoeff[5]/t[i] - ch3ocoeff[6]
		else:
			muh2 = h2coeff[7]*(1.-log(t[i])) - h2coeff[8]*t[i]/2. - h2coeff[9]*t[i]**2./6. - h2coeff[10]*t[i]**3./12. - h2coeff[11]*t[i]**4./20. + h2coeff[12]/t[i] - h2coeff[13]
			muco = cocoeff[7]*(1.-log(t[i])) - cocoeff[8]*t[i]/2. - cocoeff[9]*t[i]**2./6. - cocoeff[10]*t[i]**3./12. - cocoeff[11]*t[i]**4./20. + cocoeff[12]/t[i] - cocoeff[13]
			much3o = ch3ocoeff[7]*(1.-log(t[i])) - ch3ocoeff[8]*t[i]/2. - ch3ocoeff[9]*t[i]**2./6. - ch3ocoeff[10]*t[i]**3./12. - ch3ocoeff[11]*t[i]**4./20. + ch3ocoeff[12]/t[i] - ch3ocoeff[13]

		k0 = 1.4e-6*t[i]**(-1.2)
		k0 = k0*exp(-7800/t[i])
	
		kinf = 1.5e11*t[i]
		kinf = kinf*exp(-12880/t[i])
	
		n = p[i]/(kb*t[i])
		n = n/(100.**3.)
	
		k = k0*kinf/(k0*n+kinf)
	
		keq = muco + 3./2.*muh2 - much3o
		keq = exp(-keq)
	
		timescale[i] = n*k*xh2**(3./2.)*(p[i]/P0)**(3./2.)
		timescale[i] = keq/timescale[i]
  
	return timescale