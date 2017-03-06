/* -------------------------------------------------------------------
   File "EleSta_v.pro"

   Electrostatics - Electric scalar potential v formulation
   ------------------------------------------------------------------- 

   I N P U T
   ---------

   Global Groups :  (Extension '_Ele' is for Electric problem)
   -------------
   Domain_Ele               Whole electric domain (not used)
   DomainCC_Ele             Nonconducting regions
   DomainC_Ele              Conducting regions (not used)

   Function :
   --------
   epsr[]                   Relative permittivity

   Constraint :
   ----------
   ElectricScalarPotential  Fixed electric scalar potential
                            (classical boundary condition)

   Physical constants :
   ------------------                                               */

   eps0 = 8.854187818e-12;

Group {
  DefineGroup[ Domain_Ele, DomainCC_Ele, DomainC_Ele ];
}

Function {
  DefineFunction[ epsr ];
}

FunctionSpace {
  { Name Hgrad_v_Ele; Type Form0;
    BasisFunction {
      // v = v  s   ,  for all nodes
      //      n  n
      { Name sn; NameOfCoef vn; Function BF_Node;
        Support DomainCC_Ele; Entity NodesOf[ All ]; }
    }
    Constraint {
      { NameOfCoef vn; EntityType NodesOf; 
        NameOfConstraint ElectricScalarPotential; }
    }
  }
}


Formulation {
  { Name Electrostatics_v; Type FemEquation;
    Quantity {
      { Name v; Type Local; NameOfSpace Hgrad_v_Ele; }
    }
    Equation {
      Galerkin { [ epsr[] * Dof{Grad v} , {Grad v} ]; In DomainCC_Ele; 
                 Jacobian VolAxi; Integration GradGrad; }
    }
  }
}


Resolution {
  { Name EleSta_v;
    System {
      { Name Sys_Ele; NameOfFormulation Electrostatics_v; }
    }
    Operation { 
      Generate[Sys_Ele]; Solve[Sys_Ele]; SaveSolution[Sys_Ele];
    }
  }
}


PostProcessing {
  { Name EleSta_v; NameOfFormulation Electrostatics_v;
    Quantity {
      { Name v; 
        Value { 
          Local { [ {v} ]; In DomainCC_Ele; Jacobian VolAxi; } 
        }
      }
      { Name e; 
        Value { 
          Local { [ -{Grad v} ]; In DomainCC_Ele; Jacobian VolAxi; }
        }
      }
      { Name d; 
        Value { 
          Local { [ -eps0*epsr[] * {Grad v} ]; In DomainCC_Ele; 
                                             Jacobian VolAxi; } 
        } 
      }
      { Name C;
        Value {
          Integral { [ 2.0*Pi*epsr[] * SquNorm[{Grad v}] ]; In DomainCC_Ele;
                      Integration GradGrad; Jacobian VolAxi; }
        }
      }
    }
  }
}
