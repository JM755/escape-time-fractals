#An exploration of fractals.
#parameter: changes how the mapping works/what image is produced. e.g. zoom, resolution, colour scheme. 
#attribute: changes how these maps are evaluated.                 e.g. max_iteration, enable_cache.
import cmath

from util import *
from colormap import *
from configure import Configuration

class MultibrotAttrs(Configuration):
    max_iteration = 25
    escape        = 10
    enable_cache  = False
    enable_return = False


    #want to try: modularise fn's into own file, and use lambda d/dx. maybe leave default fn here or just specify default. 
    #then again, mapping should probably be a 'parameter' not and 'attribute'.
    @staticmethod
    def mandelbrot_map(instance):
        z_next = (instance.z_i)**(instance.exponent)+instance.z_0
        return z_next
    @staticmethod
    def julia_set(instance):
        z_next = (instance.z_i)**(instance.exponent)+exp(complex(0,pi/2))
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
    @staticmethod
    def exp_x_iy(instance):
        z_next = exp(instance.z_i)+instance.z_0
        return z_next
    @staticmethod
    def inverse_julia(instance):
        z_next = ((instance.z_i)**(2)+exp(complex(0, pi/2)))**(complex(0, -1))
        return z_next
    @staticmethod
    def gamma(instance):
        z_next = None
        return z_next
    default_fn = mandelbrot_map
    @staticmethod
    def fibonacci(instance):
        #calculate fib num @ z_0th index,  (z_0 + 1)th index
        def binet(index, iter):
            x = index+iter
            return (phi**x-(-phi)**x)/sq(5)
        z_next = binet(instance.z_0, instance.z_i)
        return z_next
    default_fn = map_map


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
        self.exponent        = complex(exponent_re,exponent_im)
        self.z_fn_string     = z_fn_string

        self._attrs     = self.get_attributes()
        self._iteration = 0
        self._cache     = [self.z_0]
        self._last_z         = None
        self._last_iteration = None
        self._set_function()


    def get_real(self):
        return self.z_i.real
    
    def get_imag(self):
        return self.z_i.imag

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
        if ((self.re_i-self.re_0)**2+(self.im_i-self.im_0)**2 <= self._attrs.escape**2) \
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
        if self._iteration == 0:
            print("No operation has yet been performed on z_0 to produce a result.")
            return -1
        else:
            self._last_iteration = self._iteration
            return self._last_iteration
        
    def get_last_z(self):
        if self._iteration == 0: 
            print("No operation has yet been performed on z_0 to produce a result##.")
            return -1
        else:
            self._last_z = self.z_i
            return self._last_z
