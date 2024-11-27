from util import *
from colormap import *
from hypercomplex import CoSystem
from configure import Configuration

from multibrot import *


class CoFractal(Hyperbrot):
    attrs = MultibrotAttrs
    @classmethod
    def get_attributes(cls):
        return cls.attrs
    def __init__(self, x_0, y_0, z_fn_string = None):
        super().__init__(x_0, y_0)

