# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

r_max = 5.0e-9
z_min = -2.475e-9
z_max = 7.475e-9
n_r = 101
n_z = 200
cut_eps = 1.0e-9

if len(sys.argv) == 3:
    v_mesh_in = sys.argv[1]
    v_grid_out = sys.argv[2]
else:
    sys.exit("Usage: python {} v_mesh_input v_grid_output".format(sys.argv[0]))

# load raw data from .pos file
print("Reading in the data...")
x1, y1, z1, x2, y2, z2, x3, y3, z3, v1, v2, v3 = np.loadtxt(v_mesh_in, unpack=True)
print("done")

x = np.append(x1,(x2,x3))
y = np.append(y1,(y2,y3))
v = np.append(v1,(v2,v3))

# define r and z range that is cut away from the raw data
# (a bit larger than the interpolation grid)
r_cut_max = r_max+cut_eps
z_cut_min = z_min-cut_eps
z_cut_max = z_max+cut_eps

# define the interpolation grid
rs = np.linspace(0.0, r_max, n_r)
zs = np.linspace(z_min, z_max, n_z)
r_grid, z_grid = np.meshgrid(rs, zs)

# mask x and y values
print("Masking")
mask1 = np.ma.masked_greater(x, r_cut_max)
mask2 = np.ma.masked_greater(y, z_cut_max)
mask3 = np.ma.masked_less(y, z_cut_min)

mask_combination = np.ma.getmask(mask1)|np.ma.getmask(mask2)|np.ma.getmask(mask3)

r0 = np.ma.masked_array(data=x,mask=mask_combination)
r = np.ma.compressed(r0)

z0 = np.ma.masked_array(data=y,mask=mask_combination)
z = np.ma.compressed(z0)

v0 = np.ma.masked_array(data=v,mask=mask_combination)
v = np.ma.compressed(v0)

# interpolate
print("Interpolating")
v_grid = griddata((r, z), v, (r_grid, z_grid), method='linear', fill_value=1.0)

r_flat = r_grid.T.ravel()
z_flat = z_grid.T.ravel()
v_flat = v_grid.T.ravel()
v_interp_data = np.column_stack((r_flat, z_flat, v_flat))
np.savetxt(v_grid_out, v_interp_data)

#plt.contourf(r_grid, z_grid, v_grid, 100)
#plt.colorbar()
#plt.show()
