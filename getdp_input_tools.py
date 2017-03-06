# coding: utf-8
#!/usr/bin/python

dielectric_function_file = "Dielectric_func.pro"

def write_dielectric_function(eps_sample, eps_air=1.0):
   out_file = open(dielectric_function_file, 'w')
   
   out_file.write("Function {\n")
   out_file.write("  epsr[Air] = {};\n".format(eps_air))
   out_file.write("  epsr[Sample] = {};\n".format(eps_sample))
   out_file.write("}\n")
   
   out_file.close()
