# coding: utf-8
#!/usr/bin/python

import math

geometry_param_file = "tip-sample_geometry_param.geo"
computational_param_file = "tip-sample_computational_param.geo"

# GMSH tolerance related options
geom_tolerance = 0.1e-10;
mesh_random_factor = 1.0e-7;
mesh_tolerance_edge_length = 0.1e-10;

def write_geometry_param(h, H_probe, R_tip, R_disc, t_disc, t_sample, t_ssample, L_container, alpha):
   beta = math.pi/2-alpha
   out_file = open(geometry_param_file, 'w')
   
   out_file.write("h = {};\n".format(h))
   out_file.write("H = {};\n".format(H_probe))
   out_file.write("R = {};\n".format(R_tip))
   out_file.write("Rd = {};\n".format(R_disc))
   out_file.write("td = {};\n".format(t_disc))
   out_file.write("ts = {};\n".format(t_sample))
   out_file.write("tss = {};\n".format(t_ssample))
   out_file.write("Lc = {};\n".format(L_container))
   out_file.write("alpha = {};\n".format(alpha))
   out_file.write("beta = {};\n".format(beta))
   
   out_file.close()
   
def write_computational_param(tip_ls, cone_ls, cantilever_ls, close_ls, far_ls,
                              sample_bottom_ls, exp_growth, cl_min, cl_max):
   out_file = open(computational_param_file, 'w')
   
   out_file.write("Geometry.Tolerance = {};\n".format(geom_tolerance))
   out_file.write("Mesh.RandomFactor = {};\n".format(mesh_random_factor))
   out_file.write("Mesh.ToleranceEdgeLength = {};\n".format(mesh_tolerance_edge_length))
   out_file.write("Mesh.CharacteristicLengthMin = {};\n".format(cl_min))
   out_file.write("Mesh.CharacteristicLengthMax = {};\n\n".format(cl_max))
   
   out_file.write("tip_ls = {};\n".format(tip_ls))
   out_file.write("cone_ls = {};\n".format(cone_ls))
   out_file.write("cantilever_ls = {};\n".format(cantilever_ls))
   out_file.write("close_ls = {};\n".format(close_ls))
   out_file.write("far_ls = {};\n".format(far_ls))
   out_file.write("sample_bottom_ls = {};\n\n".format(sample_bottom_ls))
   
   out_file.write("exp1 = {};\n".format(exp_growth))
   
   out_file.close()

def read_geometry_param():
   geometry_param = []
   with open(geometry_param_file, 'r') as in_file:
      for line in in_file:
         line = line[:len(line)-1]
         splitted = line.split()
         value = splitted[2]
         geometry_param.append(float(value[:len(value)-1]))
   return geometry_param
