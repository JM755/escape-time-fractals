#reminder: ode's with initial conditions are called IVP's: initial value problems
#import numpy as np

from dualfunction import DualFunction
from dualnumber import DualNumber
from common import *
from functions import *

class DualSystem:
    parameter_count = 2
    def __init__(self, x_0, y_0, f, g):
        self.M = DualNumber(x_0, y_0, arr([x_0, y_0], dtype = np.float64))
        self.A = DualFunction(self, f, g)
        self.iteration = 0
        self.bad_int = 0

    def do_next_map(self):
        A_x = self.A.x_func
        A_y = self.A.y_func
        M = self.M
        x_sol = A_x(M.X, M.Y, self.iteration)
        y_sol = A_y(M.X, M.Y, self.iteration)
        self.M.X = x_sol
        self.M.Y = y_sol

    def function_result_to_cmap(self):
        self.do_next_map()
        return self.M.y_(1)
    
    def do_iteration(self, max_iteration, escape, map_type):
        match map_type:
            case 'functional':
                return self.function_result_to_cmap()
            
            case 'escape_time': 
                while self.iteration < max_iteration:
                    vec_i = self.M.vec_(self.iteration)
                    vec_0 = self.M.vec_(0)
                    if norm(vec_i)<escape:
                        self.do_next_map()
                        self.iteration += 1
                    else:
                        return self.iteration
                return self.iteration
