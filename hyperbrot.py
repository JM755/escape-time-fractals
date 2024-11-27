from util import *
from colormap import *
from hypercomplex import HyperComplex
from configure import Configuration

from multibrot import *


class Hyperbrot(Multibrot):
    attrs = MultibrotAttrs
    @classmethod
    def get_attributes(cls):
        return cls.attrs
    def __init__(self, re_0, im_0, exponent_re = 2, exponent_im = 0, z_fn_string = None):
        super().__init__(re_0, im_0, exponent_re = 2, exponent_im = 0, z_fn_string = None)
        self.re_0, self.im_0 = re_0 , im_0
        self.re_i, self.im_i = self.re_0, self.im_0
        self.z_0             = HyperComplex(re_0 , im_0)
        self.z_i             = self.z_0
        self.exponent        = HyperComplex(exponent_re,exponent_im)
        self.z_fn_string     = z_fn_string
        self.bad_int = 0

        self._attrs     = self.get_attributes()
        self._iteration = 0
        self._cache     = [self.z_0]
        self._last_z         = None
        self._last_iteration = None
        self.z_function = self.hyper_z_3


    def escape_check(self):
        if abs(self.bad_int-abs(self.im_i)) == 0:
            return False
        if ((self.re_i-self.re_0)**2+(self.im_i-self.im_0)**2 <= self._attrs.escape**2) \
            and (self._iteration < self._attrs.max_iteration):
            return True
        else:
            return False

    def _update_z_i(self, update = None):
        self.z_i = HyperComplex(self.re_i, self.im_i)
        if update != None:
            self.z_i = update


    @staticmethod
    def hyper_z(self): 
        self.bad_int = 1
        if abs(self.im_i) != 1:
            new_re = (self.re_i**2+self.re_0)/(1-self.im_i**2)
            new_im = (2*self.re_i*self.im_i+self.im_0)/(1-self.im_i**2) 
            return HyperComplex(new_re, new_im)
        else:
            return HyperComplex(np.inf, np.inf)
        
    @staticmethod
    def hyper_z_band(self): 
        self.bad_int = 1
        if abs(self.im_i) != 1:
            new_re = (self.re_i**2+self.re_0)/(1+self.im_i**2)
            new_im = (2*self.re_i*self.im_i+self.im_0)/(1-self.im_i**2) 
            return HyperComplex(new_re, new_im)
        else:
            return HyperComplex(np.inf, np.inf)
        
    @staticmethod
    def hyper_z_2(self):
        new_re = (self.re_i)**2+self.re_i*(self.im_i)**2 + self.re_0
        new_im = (2*self.re_i*self.im_i)+self.im_i**3+self.im_0
        return HyperComplex(new_re, new_im)

    @staticmethod
    def hyper_z_mobius(self):
        self.bad_int = 0
        new_re = (self.re_i)**2 + (self.im_i**2)*(mobius(self._iteration)) + self.re_0
        new_im = 2*self.re_i*self.im_i + self.im_0
        return HyperComplex(new_re, new_im)
    @staticmethod
    def hyper_z_rand(self):
        self.bad_int = 0
        new_re = (self.re_i)**2 + (self.im_i**2)*(rand_bit_list[self._iteration]) + self.re_0
        new_im = 2*self.re_i*self.im_i + self.im_0
        return HyperComplex(new_re, new_im)
    
    @staticmethod
    def hyper_z_3(self): 
        self.bad_int = 1
        if abs(self.im_i) != 1: #epsilon squared = z_(n+1)+z_n ## adding z_0 appears to squash final image.
            new_re = (self.re_i**2+(self.re_i)*(self.im_i**2)+self.re_0)/(1-self.im_i**2)
            new_im = (2*self.re_i*self.im_i+self.im_0+(self.im_i**2)*(self.im_i))/(1-self.im_i**2) 
            return HyperComplex(new_re, new_im)
        else:
            return HyperComplex(np.inf, np.inf)

