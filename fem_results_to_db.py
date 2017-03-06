# coding: utf-8
#!/usr/bin/python

import sqlite3

def open_db(filename):
   con = sqlite3.connect(filename)
   cur = con.cursor()
   cur.execute("CREATE TABLE IF NOT EXISTS potential(r_tip REAL, t_sample REAL, eps_sample REAL, s REAL, r REAL, z REAL, value REAL)")
   cur.execute("CREATE TABLE IF NOT EXISTS capacitance(r_tip REAL, t_sample REAL, eps_sample REAL, s REAL, value REAL)")
   con.commit()
   return con

def close_db(db_con):
   if db_con:
      db_con.close()

def write_pot_to_db(r_tip, t_sample, eps_sample, s, pot_filename, db_con):
   pot_data = []
   with open(pot_filename, 'r') as pot_file:
      for line in pot_file:
         splitted = line.split()
         if len(splitted) < 3:
            continue
         r = float(splitted[0])
         z = float(splitted[1])
         pot = float(splitted[2])
         if pot < 1.0e-8:
            pot = 1.0
         pot_data.append((r_tip, t_sample, eps_sample, s, r, z, pot))
         
   cur = db_con.cursor()
   cur.executemany("INSERT INTO potential VALUES(?,?,?,?,?,?,?)", pot_data)
   db_con.commit()

def write_C_to_db(r_tip, t_sample, eps_sample, s, C_filename, db_con):
   C_data = []
   with open(C_filename, 'r') as C_file:
      for line in C_file:
         splitted = line.split()
         if len(splitted) < 2:
            continue
         C = float(splitted[1])
         C_data.append((r_tip, t_sample, eps_sample, s, C))
         
   cur = db_con.cursor()
   cur.executemany("INSERT INTO capacitance VALUES(?,?,?,?,?)", C_data)
   db_con.commit()
