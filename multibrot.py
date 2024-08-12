#An exploration of fractals.
#parameter: changes how the mapping works/what image is produced. e.g. zoom, resolution, colour scheme. 
#attribute: changes how these maps are evaluated.                 e.g. max_iteration, enable_cache.
from abc import ABCMeta, abstractmethod
from fractions import Fraction
import math
import cmath
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import random
import time
import os

top = plt.colormaps['ocean'].resampled(128)
#middle = plt.colormaps['afmhot_r'].resampled(128)
bottom = plt.colormaps['inferno_r'].resampled(128)

newcolors = np.vstack((top(np.linspace(0.4, 1, 48)),
                       #middle(np.linspace(0, 0.4, 8)),
                       bottom(np.linspace(0, 0.9, 128))))
newcmp = ListedColormap(newcolors, name='inferno_viridis')

twilight_cmap = plt.colormaps['twilight_shifted']
#twilight_cmap.set_under((1,1,1,0))#(color="white", alpha=0)


def randlist(max_index):
    _list = []
    for i in range(0, max_index):
        _list.append(random.randrange(-1, 1, 1))
    return _list
rand_bit_list = randlist(1000)

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
phi = (1+sq(5))/2

def isPrime(n) :
 
    if (n < 2) :
        return False
    for i in range(2, n + 1) :
        if (i * i <= n and n % i == 0) :
            return False
    return True
 
def mobius(N) :
    if (N == 1) :
        return 1
    p = 0
    for i in range(1, N + 1) :
        if (N % i == 0 and
                isPrime(i)) :
            if (N % (i * i) == 0) :
                return 0
            else :
                p = p + 1
    if(p % 2 != 0) :
        return -1
    else :
        return 1
#https://rosettacode.org/wiki/M%C3%B6bius_function#Python mobius and isprime funcs
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



class HyperComplex:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def get_real(self):
        return self.real
    def get_imag(self):
        return self.imag


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



class FractalplotAttrs(Configuration):
    pass

class Fractalplot():
    def __init__(self, re_start, re_stop, im_start, im_stop, resolution_x, resolution_y, class_type = Multibrot, enable_save = False, dpi = 227):
        self.enable_save = enable_save
        self.class_type = class_type

        self.re_start   = re_start
        self.re_stop    = re_stop
        self.im_start   = im_start
        self.im_stop    = im_stop
        self.resolution_x = resolution_x
        self.resolution_y = resolution_y
        self.dpi = dpi

        self.lin1 = np.linspace(self.re_start, self.re_stop, self.resolution_x)
        self.lin2 = np.linspace(self.im_start, self.im_stop, self.resolution_y)
        self.RE, self.IM = np.meshgrid(self.lin1, self.lin2)

        self.evaluate_all_maps = np.vectorize(self.evaluate_map)
        self.iteration_maps = self.evaluate_all_maps(self.RE, self.IM)
        self.plot()



    def plot(self):
        self.fig, self.axs = plt.subplots(layout='constrained')
        self.pc = self.axs.pcolormesh(self.RE, self.IM, self.iteration_maps, vmin=0, vmax=Multibrot.attrs.max_iteration, cmap=twilight_cmap)#'twilight_shifted') #newcmp)#'inferno_r') #

        self.axs.set_aspect('equal', adjustable='box')
        self.save_plot_to_folder(draw_features = 'off')
        self.axs.set_title('Hypercomplex Map')
        #plt.axis('on')
        #plt.show()

    def evaluate_map(self, re, im):
        return self.class_type(re, im).do_map_iteration()
    
    def make_plot_dir(self):
        #🤮
        split = os.path.split
        abspath = os.path.abspath
        self.image_path = split(split(abspath(__file__))[0])[0] 
        if not os.path.exists(self.image_path+'/plots'):
            os.mkdir(self.image_path+'/plots')
        self.image_path = self.image_path + '/plots/'

    
    def save_plot_to_folder(self, draw_features):
        if self.enable_save == True:
            self.make_plot_dir()
            plt.axis(draw_features)
            self.image_name = f'Fractal-{time.time()}.pdf'
            self.fig.savefig(self.image_path+self.image_name, format='pdf', bbox_inches = 'tight', pad_inches = 0, dpi = (self.dpi))#*dpi_scale))


# settings for hypercomplex fractal
resolution_x =2560
resolution_y =1600
res_scale = 2
maxitr = 50
bound_scale = 0.9  #default is 1.28=2560/1600/1.25
zoom = 0
location = 0
MultibrotAttrs.with_kwargs(escape = 20, max_iteration = maxitr, enable_return = True)
Hyperfractest = Fractalplot(-2.25*bound_scale-zoom, 0.75*bound_scale+zoom, -0.9375*bound_scale-zoom/1.6, 0.9375*bound_scale+zoom/1.6, resolution_x*res_scale, resolution_y*res_scale, Hyperbrot, enable_save=True)

# resolution_x = 256
# resolution_y = 256
# dpi_scale = 1
# MultibrotAttrs.with_kwargs(escape = 4, enable_return = True)
# fractest = Fractalplot(0, 2, -2, 2, resolution_x*dpi_scale, resolution_y*dpi_scale, Multibrot)

# mbp 2019 2560x1600 @ 227 dpi
#mandelbrot bounds: -2.5,0.5, -1.25, 1.25, 200
#for mbp wallpaper: (-2.5, 0.5,  -0.9375, 0.9375)*(bound_scale=1.28)
#for hypermap, maxitr =40 and escape = 4 is the default i'm using.

