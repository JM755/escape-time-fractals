from common import *

def mandelbrot_real(X, Y, i):
    return X[i]**2-Y[i]**2+X[0]
def mandelbrot_imag(X, Y, i):
    return 2*X[i]*Y[i]+Y[0]


def eisenstein_real(X, Y, i):
    _    = float()
    return X[i]**3+Y[i]**3-(3*X[i]*Y[i]*(X[i]+Y[i])/2)+X[0]-Y[0]/2
def eisenstein_imag(X,Y, i):
    _    = float()
    return (3*sqrt(3)*X[i]*Y[i]*(X[i]-Y[i])/2)+(sqrt(3)*Y[0]/2)

def nicholson_bailey_real(X, Y, i):
    a, k = float(), float()
    return k*X[i]*e**(-a*Y[i])
def nicholson_bailey_imag(X, Y, i):
    a, c = float(), float()
    return c*X[i]*(1-e**(-a*Y[i]))

def hanon_real(X, Y, i):
    A = 0.2
    return 1-A*X[i]**2+Y[i]
def hanon_imag(X, Y, i):
    B = 1.01
    return B*X[i]
     



