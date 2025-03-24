from functions import *

default_plot_parameters = {
    'max_iteration': 50,
    'escape':10,

    'f(x,y)->x' : mandelbrot_real,
    'g(x,y)->y' : mandelbrot_imag,

    'x_centrepoint': 0.25,
    'y_centrepoint': 0.00,
    'magnification': 8,

    'title': 'ET Fractal',
    'color_map' : 'twilight_shifted',
    'map_type': 'escape_time',
    'draw_features' : 'off',
    'x_resolution' : 1512,
    'y_resolution': 982,
}

meta_plot_parameters = {
    'show_plot': True,
    'save_plot': True,
    'file_format' : 'pdf',
    'bounding_box' : 'tight',
    'padding' : 0,
    'dpi' : 254,
    'axes_adjustable': 'box',
    'axes_aspect': 'equal',
    'sp_layout': 'constrained'
}