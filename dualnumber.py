import numpy as np
from common import *

class DualNumber:
    def __init__(self, x_0=0, y_0=0, v_0=arr([0, 0], dtype = np.float64)):
        self.result_cache = arr([nan, nan])
        ### Inappropriate to use None as a mask in self.result_cache because it is not a floating point number.
        ### Using None causes a weird output. e.g: [ [2 7] [np.int64(28) np.int64(70)] ]
        ### https://numpy.org/devdocs/reference/constants.html#numpy.nan
        ### https://numpy.org/doc/stable/user/misc.html

        self.x_0, self.y_0, self.v_0 =      x_0,        y_0,        v_0
        self._X,  self._Y,  self._V  = arr([x_0]), arr([y_0]), arr([v_0])

        self.x_   = lambda i: self.X[i] # i -> x_i
        self.y_   = lambda i: self.Y[i] # i -> y_i
        self.vec_ = lambda i: self.vec[i]   # i -> (x_i, y_i)

    @property
    def X(self):
        return self._X
    @property
    def Y(self):
        return self._Y
    @property
    def vec(self):
        return self._V
        
    @X.setter
    def X(self, x_result):
        X_appended = np.append(self._X, x_result)
        self._X = X_appended
        self.result_cache[0] = x_result

        if not (np.isnan(self.result_cache[0]) or isnan(self.result_cache[1])):
            self.vec = self.result_cache
    @Y.setter
    def Y(self, y_result):
        Y_appended = np.append(self._Y, y_result)
        self._Y = Y_appended
        self.result_cache[1] = y_result

        if not (np.isnan(self.result_cache[0]) or isnan(self.result_cache[1])):
            self.vec = self.result_cache
    @vec.setter
    def vec(self, vec_result):
        vec_appended = np.append(self._V, arr([vec_result]), axis = 0)
        self._V = vec_appended
        self.result_cache = arr([nan, nan])
        self._X, self._Y = arr(self._V[:,0]), arr(self._V[:,1]) # V[:,k] is kth column of V.