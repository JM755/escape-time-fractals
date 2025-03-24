import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import os
import time

from coupledfractals import DualSystem
from plotparams import *
from common import *

class Plotter:
    def __init__(self, parameters, meta_parameters):
        self.p = parameters
        self.mp = meta_parameters
        self._f = self.p['f(x,y)->x']
        self._g = self.p['g(x,y)->y']
        self.x_space, self.y_space= self.mk_x_space(), self.mk_y_space()
        self.x_mesh, self.y_mesh = np.meshgrid(self.x_space, self.y_space)
        self.map_mesh = v_ize(self.evaluate_map_single)
        self.result = self.map_mesh(self.x_mesh, self.y_mesh)
        self.plot()

    def mk_x_space(self):
        x,y = 0,1
        centre, mag, x_res, y_res = self.p['x_centrepoint'], self.p['magnification'], self.p['x_resolution'], self.p['y_resolution']
        x_scale = x_res/y_res
        x_start, x_stop = centre-x_scale*mag/2, centre+x_scale*mag/2
        return np.linspace(x_start, x_stop, x_res)

    def mk_y_space(self):
        x,y=0,1
        centre, mag, y_res = self.p['y_centrepoint'], self.p['magnification'], self.p['y_resolution']
        y_start, y_stop = centre-mag/2, centre+mag/2
        return np.linspace(y_start, y_stop, y_res)
    
    
    def evaluate_map_single(self, x_0, y_0):
        map_type = self.p['map_type']
        max_iter, escape = self.p['max_iteration'], self.p['escape']
        single_mapping = DualSystem(x_0, y_0, self._f, self._g)
        return single_mapping.do_iteration(max_iter, escape, map_type)

    def show_graph(self):
        title = self.p['title']
        ax_aspect, ax_adjust = self.mp['axes_aspect'], self.mp['axes_adjustable']
        if self.p['draw_features'] == 'on':
            self.axs.set_aspect(ax_aspect, adjustable = ax_adjust)
            self.axs.set_title(title)
            self.fig.colorbar(self.pc, ax=self.axs)
        if self.p['draw_features'] == 'off':
            self.axs.axis('off')
        if self.mp['show_plot']:
            plt.show()

    def make_plot_dir(self): #🤮
        split = os.path.split
        abspath = os.path.abspath
        self.image_path = split(split(abspath(__file__))[0])[0] 
        if not os.path.exists(self.image_path+'/plots'):
            os.mkdir(self.image_path+'/plots')
        self.image_path = self.image_path + '/plots/'

    
    def save_graph(self):
        if self.mp['save_plot']:
            self.make_plot_dir()
            plt.axis(self.p['draw_features'])
            self.image_name = f'Fractal-{time.time()}.pdf'
            self.fig.savefig(self.image_path+self.image_name, format=self.mp['file_format'], bbox_inches = self.mp['bounding_box'], pad_inches = self.mp['padding'], dpi = self.mp['dpi'])

    def plot(self):
        max_iter, color_map = self.p['max_iteration'], self.p['color_map']
        sp_layout = self.mp['sp_layout']
        x_mesh, y_mesh, result = self.x_mesh, self.y_mesh, self.result

        self.fig, self.axs = plt.subplots(layout=sp_layout)
        self.pc = self.axs.pcolormesh(x_mesh, y_mesh, result, vmin=1, vmax=max_iter, cmap=color_map)
        self.show_graph()
        self.save_graph()
        
fractal_map = Plotter(default_plot_parameters, meta_plot_parameters)