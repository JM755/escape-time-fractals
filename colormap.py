import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

top = plt.colormaps['ocean'].resampled(128)
#middle = plt.colormaps['afmhot_r'].resampled(128)
bottom = plt.colormaps['inferno_r'].resampled(128)

newcolors = np.vstack((top(np.linspace(0.4, 1, 48)),
                       #middle(np.linspace(0, 0.4, 8)),
                       bottom(np.linspace(0, 0.9, 128))))
newcmp = ListedColormap(newcolors, name='inferno_viridis')

twilight_cmap = plt.colormaps['twilight_shifted']
#twilight_cmap.set_under((1,1,1,0))#(color="white", alpha=0)

