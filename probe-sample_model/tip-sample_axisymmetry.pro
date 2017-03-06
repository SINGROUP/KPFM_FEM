Group {
  Probe = Region[1000];
  Sample = Region[1001];
  Air = Region[1002];
  Ground = Region[1003];
  
  // Non-conducting domain
  DomainCC_Ele = Region[{Sample,Air}];
}

//Function {
  // Relative permittivities
//  epsr[Air] = 1.0;
//  epsr[Sample] = 5.9;
//}

// Relative permittivities
Include "Dielectric_func.pro"

Constraint {
  { Name ElectricScalarPotential; Type Assign;
    Case {
      { Region Ground; Value 0.0; }
      { Region Probe; Value 1.0; }
    }
  }
}

Include "Jacobian_Lib.pro"
Include "Integration_Lib.pro"
Include "EleSta_v.pro"


// Output results
cut_length_r = 5.0e-9;
cut_length_z = 10.1e-9;

PostOperation {
  { Name Map; NameOfPostProcessing EleSta_v;
     Operation {
       Print [ v, OnElementsOf DomainCC_Ele, File "tip-sample_v.pos" ];
       //Print [ e, OnElementsOf DomainCC_Ele, File "tip-sample_e.pos" ];
     }
  }
  { Name Map_interp; NameOfPostProcessing EleSta_v;
     Operation {
       Print [ v, OnElementsOf DomainCC_Ele, Format SimpleTable, File "tip-sample_v.pos" ];
     }
  }
  { Name V_grid; NameOfPostProcessing EleSta_v;
     Operation {
       Print [ v, OnPlane {{0,-cut_length_z/4.0,0}{cut_length_r,-cut_length_z/4.0,0}{0,3*cut_length_z/4.0,0}} {100,202}, Format SimpleTable, File "v.txt" ];
     }
  }
  { Name E_field_line; NameOfPostProcessing EleSta_v;
     Operation {
       Print [ e, OnLine {{0,1.0e-10,0}{cut_length_r,1.0e-10,0}} {100}, Format SimpleTable, File "line_e.txt" ];
     }
  }
  { Name Capacitance; NameOfPostProcessing EleSta_v;
    Operation {
      Print [ C[ #{Air,Sample} ], OnGlobal, Format SimpleTable, File "C.txt" ];
    }
  }
}
