# coding: utf-8
#!/usr/bin/python

import os, sys, subprocess, shutil
import sqlite3
import numpy as np
from gmsh_input_tools import write_geometry_param, write_computational_param
from getdp_input_tools import write_dielectric_function
from fem_results_to_db import open_db, close_db, write_pot_to_db, write_C_to_db

geometry_file = "tip-sample_axisymmetry.geo"
problem_def_file = "tip-sample_axisymmetry.pro"
resolution = "EleSta_v"
post_processing = ["Capacitance", "V_grid"]
pot_filename = "v.txt"
C_filename = "C.txt"

if len(sys.argv) == 2:
   array_job = False
   db_name = sys.argv[1]
else:
   array_job = True

# Macroscopic tip-sample distance range
s_min = 0.7e-9
s_max = 4.9e-9
s_delta = 2.0e-10

# Dielectric constant
eps_sample = 5.9

# Geometry parameters (units: m)
H_probe = 15.0e-6
R_tip = 20.0e-9
R_disc = 35.0e-6
t_disc = 0.5e-6
t_sample = 1.0e-3
t_ssample = min(3*H_probe, 0.5*t_sample)
L_container = 1.0e6*R_tip
alpha = 15.0*np.pi/180.0

# Characteristic lenght scales of the mesh
mesh_characteristic_length_min = 0.1e-10
mesh_characteristic_length_max = 1.0e-3
tip_ls = 0.5e-10
cone_ls = 0.1e-7
cantilever_ls = 2.0e-7
close_ls = 1.0e-6
far_ls = 0.5e-3
sample_bottom_ls = 0.5*far_ls

# Exponential growth parameter of the mesh
exp_growth = 1.15

# Choose preparing an array job or running sequentially
if array_job:
   s_list = np.arange(s_min,s_max+0.5*s_delta,s_delta)
   for i in range(len(s_list)):
      os.mkdir("job_{}".format(i))
      os.chdir("job_{}".format(i))
      shutil.copy("../{}".format(geometry_file), '.')
      shutil.copy("../{}".format(problem_def_file), '.')
      
      # Write mesh generation parameters to file
      write_computational_param(tip_ls, cone_ls, cantilever_ls, close_ls,
                                 far_ls, sample_bottom_ls, exp_growth, 
                                 mesh_characteristic_length_min,
                                 mesh_characteristic_length_max)
      # Write dielectric constants to file
      write_dielectric_function(eps_sample)
      # Write geometry parameters to file
      write_geometry_param(s_list[i], H_probe, R_tip, R_disc, t_disc, t_sample,
                              t_ssample, L_container, alpha)
      os.chdir('..')

else:
   # Write mesh generation parameters to file
   write_computational_param(tip_ls, cone_ls, cantilever_ls, close_ls,
                              far_ls, sample_bottom_ls, exp_growth, 
                              mesh_characteristic_length_min,
                              mesh_characteristic_length_max)
   # Write dielectric constants to file
   write_dielectric_function(eps_sample)
   
   # Get database connection
   db_con = None
   try:
      db_con = open_db(db_name)

      for s in np.arange(s_min,s_max+0.5*s_delta,s_delta):
         # Write geometry parameters to file
         write_geometry_param(s, H_probe, R_tip, R_disc, t_disc, t_sample,
                              t_ssample, L_container, alpha)
                              
         subprocess.call(["gmsh", geometry_file, "-2"])
         subprocess.call(["getdp", problem_def_file, "-solve", resolution,
                           "-pos", post_processing[0]])
         
         #write_pot_to_db(R_tip, t_sample, eps_sample, s, pot_filename, db_con)
         write_C_to_db(R_tip, t_sample, eps_sample, s, C_filename, db_con)

   except sqlite3.Error, e:
      print "Error {}:".format(e.args[0])
      sys.exit(1)
   finally:
      close_db(db_con)
