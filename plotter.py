import numpy as np
import matplotlib.pyplot as plt
import time
import os

from util import *
from colormap import *
from hypercomplex import HyperComplex
from configure import Configuration

from multibrot import *
from hyperbrot import *


class FractalplotAttrs(Configuration):
    pass

class Fractalplot():
    def __init__(self, re_start, re_stop, im_start, im_stop, resolution_x, resolution_y, class_type = Multibrot, enable_save = False, enable_plot = True, dpi = 227):
        self.enable_save = enable_save
        self.enable_plot = enable_plot
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
        if self.enable_plot:
            plt.axis('on')
            plt.show()

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
resolution_x =256
resolution_y =160
res_scale = 1
maxitr = 50
bound_scale = 0.9  #default is 1.28=2560/1600/1.25
zoom = 0
location = 0
MultibrotAttrs.with_kwargs(escape = 20, max_iteration = maxitr, enable_return = True)
Hyperfractest = Fractalplot(-2.25*bound_scale-zoom, 0.75*bound_scale+zoom, -0.9375*bound_scale-zoom/1.6, 0.9375*bound_scale+zoom/1.6, resolution_x*res_scale, resolution_y*res_scale, Hyperbrot, enable_save=False)

# resolution_x = 256
# resolution_y = 256
# dpi_scale = 1
# MultibrotAttrs.with_kwargs(escape = 4, enable_return = True)
# fractest = Fractalplot(0, 2, -2, 2, resolution_x*dpi_scale, resolution_y*dpi_scale, Multibrot)

# mbp 2019 2560x1600 @ 227 dpi
#mandelbrot bounds: -2.5,0.5, -1.25, 1.25, 200
#for mbp wallpaper: (-2.5, 0.5,  -0.9375, 0.9375)*(bound_scale=1.28)
#for hypermap, maxitr =40 and escape = 4 is the default i'm using.
