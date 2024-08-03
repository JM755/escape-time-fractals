#An exploration of fractals.
from abc import ABCMeta, abstractmethod
from fractions import Fraction
import math
import cmath
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import random

pi = cmath.pi
e = cmath.e
exp = cmath.exp
def ln(x):
    return cmath.log(x)
ru = random.uniform
fac=math.factorial
sq = math.sqrt
ceil = math.ceil
floor = math.floor

def prime_sieve(end):
    end = end+1
    integers = np.arange(0, end)
    composite_integers  = np.array([0, 1])
    for i in range(2, ceil(sq(end))):
        if i not in composite_integers:
            mult_range = np.arange(i**2, end, i)
            composite_integers = np.union1d(composite_integers, mult_range)
    integers = np.delete(integers, composite_integers)
    return integers
print(prime_sieve(30))

# def is_prime(number):
#     for i in range(2, sqrt(number))

def get_factors(number, exponent = 0, include_trivial=False):
    pass

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
    enable_return = False

    @staticmethod
    def mandelbrot_map(instance):
        z_next = (instance.z_i)**(instance.exponent)+instance.z_0
        return z_next
    @staticmethod
    def multibrot_iter_map(instance):
        z_next = (instance.z_i)**(instance.get_iteration())+instance.z_0
        return z_next
    @staticmethod
    def sq_iter_map(instance):
        z_next = (instance.z_i)**(sq(instance.get_iteration()))+instance.z_0
        return z_next
    @staticmethod
    def map_map(instance):
        z_next = (instance.z_i)**(instance.z_i)+instance.z_0
        return z_next
    @staticmethod
    def map_z_0(instance):
        z_next = (instance.z_i)**(instance.z_0)+instance.z_0
        return z_next
    def other(instance):
        z_next = (instance.z_i)**(2)+2*instance.z_i+instance.z_0
        return z_next
    #default_fn = mandelbrot_map
    #default_fn = multibrot_iter_map
    #default_fn = sq_iter_map
    default_fn = mandelbrot_map

    # def rec_relation_n_plus_1(self):
    #     if abs(self.hc) != 1:

    #         print(self.hc)
    #         new_re = (self.re**2+self.c_re)/(1-self.hc**2)
    #         new_hc = (2*self.re*self.hc+self.c_hc)/(1-self.hc**2) 
    #         self.re = new_re
    #         self.hc = new_hc
    #         self.cache.append((new_re, new_hc))
    #     else:
    #         self.passes = self.depth

    # def rec_relation_n_plus_k(self, depth):
    #     for i in range(1, depth):
    #         self.rec_relation_n_plus_1()
    #     return self.get_cache()
"""
#TEST FOR Multibrot
MultibrotAttrs.with_kwargs(escape = 4, max_iteration = 10000, boobies=80085) #exclude this line for default vals.
test = Multibrot(-1, 0)
print(test.do_map_iteration())
"""

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
        self.exponent        = complex(exponent_re,exponent_im)  #(random.uniform(0, 2), random.uniform(0, 2)) #delete when done screwing around# complex(exponent_re, exponent_im)
        self.z_fn_string     = z_fn_string

        self._attrs     = self.get_attributes()
        self._iteration = 0
        self._cache     = [self.z_0]
        self._last_z         = None
        self._last_iteration = None

        self._set_function()

    def get_iteration(self):
        return self._iteration

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

    def _next_map(self):
        z_next = self.z_function(self)
        re_next, im_next = z_next.real, z_next.imag
        self._update_z_i(z_next)
        self._update_parts((re_next, im_next))
        self._update_cache()
        self._update_iteration()

    def escape_check(self):
        if (self.re_i**2+self.im_i**2 <= self._attrs.escape**2) \
            and (self._iteration < self._attrs.max_iteration):
            return True
        else:
            return False

    def do_map_iteration(self ):
        while self.escape_check():
            self._next_map()
        if self._attrs.enable_return:
            return self.get_last_iteration()
            
    def get_last_iteration(self):
        # vvv for when this ^^^ function is invoked without do_map_iteration first.
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
            return self._last_z

class FractalplotAttrs(Configuration):
    pass

class Fractalplot():
    def __init__(self, re_start, re_stop, im_start, im_stop, resolution):
        self.re_start   = re_start
        self.re_stop    = re_stop
        self.im_start   = im_start
        self.im_stop    = im_stop
        self.resolution = resolution

        self.lin1 = np.linspace(self.re_start, self.re_stop, resolution)
        self.lin2 = np.linspace(self.im_start, self.im_stop, resolution)
        self.RE, self.IM = np.meshgrid(self.lin1, self.lin2)
        self.evaluate_all_maps = np.vectorize(self.evaluate_map)
        self.iteration_maps = self.evaluate_all_maps(self.RE, self.IM)

        fig, axs = plt.subplots(layout='constrained')
        pc = axs.pcolormesh(self.RE, self.IM, self.iteration_maps, vmin=0, vmax=maxitr, cmap='twilight_shifted')
        axs.set_title('Mandelbrot Set')
        plt.show()

    def evaluate_map(self, re, im):
        return Multibrot(re, im, ln(pi), pi/2).do_map_iteration()

maxitr =25
MultibrotAttrs.with_kwargs(escape = 10, max_iteration = maxitr, enable_return = True)
#fractest = Fractalplot(-1,2.7, -1, 1, 1000)


#mandelbrot bounds: -2.5,0.5, -1.25, 1.25, 200