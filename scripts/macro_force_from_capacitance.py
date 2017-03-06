# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import sqlite3

eps0 = 8.8541878176e-12
result_file = "macro_force_vs_s.txt"

if len(sys.argv) != 2:
   sys.exit("Usage: python macro_force_from_capacitance.py <database_file>")
db_name = sys.argv[1]

s_list = []
C_list = []

con = sqlite3.connect(db_name)
try:
   cur = con.cursor()
   cur.execute("SELECT s, value FROM capacitance ORDER BY s")
   rows = cur.fetchall()
   for row in rows:
      s_list.append(row[0])
      C_list.append(row[1])
   
except sqlite3.Error, e:
   print "Error {}:".format(e.args[0])
   sys.exit(1)
finally:
   if con:
      con.close()

force_vs_s_list = []
ds0 = s_list[2]-s_list[0]
for i in range(2, len(s_list)-1,2):
   ds1 = s_list[i+2]-s_list[i]
   force = 0.5*(C_list[i+2]-C_list[i-2])/(ds0+ds1)
   force_vs_s_list.append((s_list[i], force))
   ds0 = ds1

out_file = open(result_file, 'w')
for force_vs_s in force_vs_s_list:
   out_file.write("{}  {}\n".format(force_vs_s[0], force_vs_s[1]/eps0))
