#An exploration of fractals.
from abc import ABCMeta, abstractmethod
from fractions import Fraction
import math
import cmath
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import random
import time
import os



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
    def __init__(self, re_start, re_stop, im_start, im_stop, resolution_x, resolution_y):
        self.re_start   = re_start
        self.re_stop    = re_stop
        self.im_start   = im_start
        self.im_stop    = im_stop
        self.resolution_x = resolution_x
        self.resolution_y = resolution_y
        

        self.lin1 = np.linspace(self.re_start, self.re_stop, self.resolution_x)
        self.lin2 = np.linspace(self.im_start, self.im_stop, self.resolution_y)
        self.RE, self.IM = np.meshgrid(self.lin1, self.lin2)
        self.evaluate_all_maps = np.vectorize(self.evaluate_map)
        self.iteration_maps = self.evaluate_all_maps(self.RE, self.IM)

        self.make_plot_dir()

        self.fig, self.axs = plt.subplots(layout='constrained')
        self.pc = self.axs.pcolormesh(self.RE, self.IM, self.iteration_maps, vmin=0, vmax=maxitr, cmap='twilight_shifted')

        self.axs.set_aspect('equal', adjustable='box')
        self.save_plot_to_folder(draw_features = 'off')
        self.axs.set_title('Mandelbrot Set')
        plt.axis('on')
        #plt.show()

    def evaluate_map(self, re, im):
        return Multibrot(re, im).do_map_iteration()
    
    def make_plot_dir(self):
        #🤮
        split = os.path.split
        abspath = os.path.abspath
        self.image_path = split(split(abspath(__file__))[0])[0] 
        if not os.path.exists(self.image_path+'/plots'):
            os.mkdir(self.image_path+'/plots')
        self.image_path = self.image_path + '/plots/'

    
    def save_plot_to_folder(self, draw_features):
        plt.axis(draw_features)
        self.image_name = f'Fractal-{time.time()}.svg'
        self.fig.savefig(self.image_path+self.image_name, format='svg', bbox_inches = 'tight', pad_inches = 0) #dpi = (mbp_dpi*dpi_scale))

resolution_x = 2560*3
resolution_y = 1600*3
#mbp_dpi = 300
#dpi_scale = 3
maxitr = 25
MultibrotAttrs.with_kwargs(escape = 10, max_iteration = maxitr, enable_return = True)
fractest = Fractalplot(-2.5, 0.5, -1.25, 1.25, resolution_x, resolution_y) #resolution_x*dpi_scale, resolution_y*dpi_scale)#resolution)
# mbp 2019 2560x1600 @ 227 dpi
#mandelbrot bounds: -2.5,0.5, -1.25, 1.25, 200



