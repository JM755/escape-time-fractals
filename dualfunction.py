import numpy as np
from common import *

class DualFunction:
    def __init__(self, master=None, f=None, g=None):
        self.master = master
        self._x_func, self._y_func, self._xy_vec = f, g, arr([f, g])
        self.id_func = lambda anything: 0 ### id_func := anything -> 0

    @property
    def x_func(self):
        return self._x_func
    @property
    def y_func(self):
       return self._y_func
    @property
    def xy_vec(self):
        return self._xy_vec
    
    @x_func.setter
    def x_func(self, fn):
        self._x_func = fn
        self._xy_vec[0] = fn
    @y_func.setter
    def y_func(self, fn):
        self._y_func = fn
        self._xy_vec[1] = fn
    @xy_vec.setter
    def xy_vec(self, fn_0, fn_1):
        self._x_func, self._y_func = fn_0, fn_1
        self._xy_vec = fn_0, fn_1
