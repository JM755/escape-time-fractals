#An exploration of fractals.
from abc import ABCMeta, abstractmethod
from fractions import Fraction
import math
import cmath
import numpy as np
import matplotlib.pyplot as plt


pi = cmath.pi
e = cmath.e
exp = cmath.exp
def ln(x):
    return cmath.log(x)

class Configuration(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def with_kwargs(cls, **attrs):
        for arg in attrs:
            if hasattr(cls, arg):
                setattr(cls, arg, attrs[arg])
            else:
                print(f"Attribute: \'{arg}\' does not exist in this class, and has been ignored.")

class MultibrotAttrs(Configuration):
    max_iteration = 1000
    escape        = 2
    enable_cache  = False
    """escape (int), max_iteration (int), (enable_cache) (bool), default_z_function"""

    @staticmethod
    def mandelbrot_map(instance):
        z_next = (instance.z_i)**(instance.exponent)+instance.z_0
        return z_next
    default_fn = mandelbrot_map

class Multibrot():  
    attrs = MultibrotAttrs
    @classmethod
    def get_attributes(cls):
        return cls.attrs

    def __init__(self, re_0, im_0, exponent_re = 2, exponent_im = 0, z_fn_string = None):
        self.re_0, self.im_0 = re_0 , im_0
        self.re_i, self.im_i = self.re_0, self.im_0
        self.z_0             = complex(re_0 , im_0)
        self.z_i             = self.z_0
        self.exponent        = complex(exponent_re, exponent_im)
        self.z_fn_string     = z_fn_string

        self._attrs     = self.get_attributes()
        self._iteration = 0
        self._cache     = [self.z_0]
        self._last_z         = None
        self._last_iteration = None

        self._set_function()
    
    def _set_function(self):
        if self.z_fn_string == None:
            self.z_function = self.attrs.default_fn 
        else:
            print("alternative within Multibrot._set_function has not been implemented yet.")

    def _update_z_i(self, update = None):
        self.z_i = complex(self.re_i, self.im_i)
        if update != None:
            self.z_i = update

    def _update_parts(self, update_real = None, update_imag = None):
        self.re_i, self.im_i = self.z_i.real, self.z_i.imag
        if ((update_real != None) and (update_imag != None)):
            self.re_i, self.im_i = update_real, update_imag

    def _update_cache(self):
        if self._attrs.enable_cache:
            self._cache.append(self.z_i)
    
    def _update_iteration(self):
        self._iteration = self._iteration + 1

    def _mapper(self):
        z_next = self.z_function(self)
        re_next, im_next = z_next.real, z_next.imag
        self._update_z_i(z_next)
        self._update_parts((re_next, im_next))
        self._update_cache()
        self._update_iteration()

    def escape_check(self):
        if (self.re_i**2+self.im_i**2 <= self._attrs.escape) \
            and (self._iteration < self._attrs.max_iteration):
            return True
        else:
            return False

    def map_iterator(self):
        while self.escape_check():
            self._mapper()
        return self.get_last_iteration()
            
    def get_last_iteration(self):
        # vvv for when this ^^^ function is invoked without map_iterator first.
        if self._iteration == 0:
            print("No operation has yet been performed on z_0 to produce a result.")
            return -1
        else:
            self._last_iteration = self._iteration
            return self._last_iteration
    def get_last_z(self):
        if self._iteration == 0: 
            print("No operation has yet been performed on z_0 to produce a result.")
            return -1
        else:
            self._last_z = self.z_i


#TEST FOR Multibrot
# MultibrotAttrs.with_kwargs(escape = 4, max_iteration = 10000, boobies=80085) #exclude this line for default vals.
# test = Multibrot(-1, 0)
# print(test.map_iterator())




"""
class FractalplotAttrs(Configuration):
    pass

class Fractalplot():
    def __init__(self, re_start, re_stop, im_start, im_stop, resolution):
        self.re_start   = re_start
        self.re_stop    = re_stop
        self.im_start   = im_start
        self.im_stop    = im_stop
        self.resolution = resolution

        self.ITER = []

        self.lin1 = np.linspace(self.re_start, self.re_stop, resolution)
        self.lin2 = np.linspace(self.im_start, self.im_stop, resolution)
        self.RE, self.IM = np.meshgrid(self.lin1, self.lin2)

        # self.bulk_eval()
        # self.graph_colourmap()


fractest = Fractalplot(-1, 1, -1, 1, 3)
print(fractest.RE, '\n\n', fractest.IM)
"""