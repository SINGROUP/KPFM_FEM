# coding: utf-8
#!/usr/bin/python

import sys, os
import sqlite3
from fem_results_to_db import open_db, close_db, write_pot_to_db, write_C_to_db
from gmsh_input_tools import read_geometry_param

eps_sample = 5.9
pot_filename = "v.txt"
C_filename = "C.txt"

if len(sys.argv) != 3:
   sys.exit("Usage: python fem_results_collect.py <database_file> <result_set_size>")
db_name = sys.argv[1]
n_results = int(sys.argv[2])

# Get database connection
db_con = None
try:
   db_con = open_db(db_name)

   for i in range(n_results):
      print("Collecting results of job_{}".format(i))
      os.chdir("job_{}".format(i))
      geometry_param = read_geometry_param()
      s = geometry_param[0]
      R_tip = geometry_param[2]
      t_sample = geometry_param[5]
      
      write_pot_to_db(R_tip, t_sample, eps_sample, s, pot_filename, db_con)
      write_C_to_db(R_tip, t_sample, eps_sample, s, C_filename, db_con)
      os.chdir('..')

except sqlite3.Error as e:
   print("Error {}:".format(e.args[0]))
   sys.exit(1)
finally:
   close_db(db_con)
