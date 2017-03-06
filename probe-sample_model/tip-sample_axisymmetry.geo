// Geometry related parameters
Include "tip-sample_geometry_param.geo";

// Mesh size and precision related parameters
Include "tip-sample_computational_param.geo";

// Geometry of the probe
p = newp;
Point(p) = {0, h, 0, tip_ls};
Point(p+1) = {R*Sin(beta), h+R-R*Cos(beta), 0, tip_ls};
Point(p+2) = {R*Sin(beta)+H*Tan(alpha), h+R-R*Cos(beta)+H, 0, 0.5*cantilever_ls};
Point(p+3) = {Rd-0.2*td, h+R-R*Cos(beta)+H, 0, cone_ls};
Point(p+4) = {Rd-0.2*td, h+R-R*Cos(beta)+H+td, 0, cone_ls};
Point(p+5) = {0, h+R-R*Cos(beta)+H+td, 0, cantilever_ls};
Point(p+6) = {0, h+R, 0, tip_ls};
Point(p+7) = {Rd, h+R-R*Cos(beta)+H+0.2*td, 0, cone_ls};
Point(p+8) = {Rd, h+R-R*Cos(beta)+H+(1.0-0.2)*td, 0, cone_ls};
Point(p+9) = {Rd-0.2*td, h+R-R*Cos(beta)+H+0.2*td, 0, cone_ls};
Point(p+10) = {Rd-0.2*td, h+R-R*Cos(beta)+H+(1.0-0.2)*td, 0, cone_ls};
p_probe_disc_edge = p+3;
p_probe_top = p+5;
p_probe_bottom = p;

l = newl;
Circle(l) = {p,p+6,p+1};
Line(l+1) = {p+1,p+2};
Line(l+2) = {p+2,p+3};
Circle(l+3) = {p+3,p+9,p+7};
Line(l+4) = {p+7,p+8};
Circle(l+5) = {p+8,p+10,p+4};
//Line(l+3) = {p+3,p+4};
Line(l+6) = {p+4,p+5};
line_probe = {l:l+6};

// Small air cylinder
p = newp;
Point(p) = {0, 0, 0, 4*tip_ls};
Point(p+1) = {3*Rd, 0, 0, close_ls};
Point(p+2) = {3*Rd, 4*H, 0, 2*close_ls};
Point(p+3) = {0, 4*H, 0, close_ls};
p_sample_center = p;
p_scyl_edge = p+1;
p_scyl_top = p+3;

l = newl;
Line(l) = {p_probe_bottom,p};
Line(l+1) = {p,p+1};
Line(l+2) = {p+1,p+2};
Line(l+3) = {p+2,p+3};
Line(l+4) = {p+3,p_probe_top};
line_sample_scyl_top = l+1;
line_scyl_edge = l+2;
line_scyl_top = l+3;
symmetry_axis[] = {l,l+4};

ll = newll;
Line Loop(ll) = {l:l+4, -line_probe[]};
s = news;
Plane Surface(s) = {ll};
surf_air_scyl = s;


// Large air cylinder
p = newp;
Point(p) = {Lc, 0, 0, far_ls};
Point(p+1) = {Lc, Lc, 0, 2*far_ls};
Point(p+2) = {0, Lc, 0, far_ls};
p_sample_edge = p;

l = newl;
Line(l) = {p_scyl_edge,p};
Line(l+1) = {p,p+1};
Line(l+2) = {p+1,p+2};
Line(l+3) = {p+2,p_scyl_top};
line_sample_lcyl_top = l;
symmetry_axis[] += {l+3};

ll = newll;
Line Loop(ll) = {l:l+3, -line_scyl_top, -line_scyl_edge};
s = news;
Plane Surface(s) = {ll};
surf_air_lcyl = s;


// Small sample cylinder
p = newp;
Point(p) = {0, -3*H, 0, 2*close_ls};
Point(p+1) = {3*Rd, -3*H, 0, 4*close_ls};
p_sample_scyl_bottom_axis = p;
p_sample_scyl_bottom_edge = p+1;

l = newl;
Line(l) = {p_sample_center,p};
Line(l+1) = {p,p+1};
Line(l+2) = {p+1,p_scyl_edge};
line_sample_scyl_bottom = l+1;
line_sample_scyl_edge = l+2;
symmetry_axis[] += {l};

ll = newll;
Line Loop(ll) = {l:l+2, -line_sample_scyl_top};
s = news;
Plane Surface(s) = {ll};
surf_sample_scyl = s;


// Large sample cylinder
p = newp;
Point(p) = {0, -ts, 0, far_ls};
Point(p+1) = {Lc, -ts, 0, far_ls};

l = newl;
Line(l) = {p_sample_scyl_bottom_axis, p};
Line(l+1) = {p, p+1};
Line(l+2) = {p+1, p_sample_edge};
symmetry_axis[] += {l};

ll = newll;
Line Loop(ll) = {l:l+2, -line_sample_lcyl_top, -line_sample_scyl_edge, -line_sample_scyl_bottom};
s = news;
Plane Surface(s) = {ll};
surf_sample_lcyl = s;


// Back-plate and infinite boundary
line_inf[] = CombinedBoundary{ Surface{surf_air_scyl,surf_air_lcyl,surf_sample_scyl,surf_sample_lcyl}; };
line_inf[] -= {-line_probe[], symmetry_axis[]};


// Mesh size fields
a_tip = (far_ls-tip_ls)/Lc^exp1;
b_tip = tip_ls;
a_cantilever = (1.1*far_ls-cone_ls)/Lc^exp1;
b_cantilever = cone_ls;
Printf("exp1: %g", exp1);
Printf("tip_ls: %g", tip_ls);
Printf("far_ls: %g", far_ls);
Printf("s: %g", h);

Field[1] = Box;
Field[1].VIn = a_tip;
Field[1].VOut = 1.4*a_tip;
Field[1].XMin = -1e-9;
Field[1].XMax = Lc+1e-9;
Field[1].YMin = -1e-9;
Field[1].YMax = Lc+1e-9;
Field[1].ZMin = 0;
Field[1].ZMax = Lc+1e-9;

Field[2] = MathEval;
Field[2].F = Sprintf("F1*Sqrt(x^2+(y-%g)^2+z^2)^%g + %g", h, exp1, b_tip);

Field[3] = MathEval;
Field[3].F = Sprintf("%g*Sqrt((x-%g)^2+(y-%g)^2+z^2)^%g + %g", a_cantilever, Rd, h+R-R*Cos(beta)+H+0.2*td, exp1, b_cantilever);

Field[4] = MathEval;
Field[4].F = Sprintf("%g*Sqrt((x-%g)^2+(y-%g)^2+z^2)^%g + %g", a_cantilever, R*Sin(beta)+H*Tan(alpha), h+R-R*Cos(beta)+H, exp1, b_cantilever);

Field[5] = Min;
Field[5].FieldsList = {2, 3};

Background Field = 5;


// Define the physical objects
PROBE = 1000;
SAMPLE = 1001;
AIR = 1002;
GROUND = 1003;
Physical Line(PROBE) = {line_probe[]};
Physical Surface(SAMPLE) = {surf_sample_scyl,surf_sample_lcyl};
Physical Surface(AIR) = {surf_air_scyl,surf_air_lcyl};
Physical Line(GROUND) = {line_inf[]};



