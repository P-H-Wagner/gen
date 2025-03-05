import numpy as np
from uncertainties import ufloat



tau_scale    = ufloat(0.1739, 0.0004)
dsStar_scale = ufloat(0.936 , 0.004 ) + ufloat(0.0577, 0.0035) 
ds2457_scale = ufloat(0.18  , 0.04  ) + ufloat(0.48  , 0.11  ) + ufloat(0.043, 0.013) + ufloat(0.037, 0.05) + ufloat(0.022, 0)

def print_br(dictionary, name):

  print(f" -------- {name} --------- ")

  output = dictionary.copy()

  for key in dictionary.keys():
    
    if "MyTau"    in key: output[key] *= tau_scale
    if "MyDs*"    in key: output[key] *= dsStar_scale
    if "MyDs2457" in key: output[key] *= ds2457_scale

  max_key_length = max(len(key) for key in output)

  for key, value in output.items():
    print(f"{key:<{max_key_length}}: {value}")



#define dict for each mom
decays_sig =  {

"MyDs-_mu+_nu"     : ufloat(0.0231 , 0.0021 ),
"MyDs*-_mu+_nu"    : ufloat(0.052  , 0.005  ),
"MyDs-_MyTau+_nu"  : ufloat(0.0231 , 0.0021 ), # since r  = 1
"MyDs*-_MyTau+_nu" : ufloat(0.052  , 0.005  ), # since r* = 1

}


decays_bs = {

"ds+_MyDs-"             : 0.5 * ufloat(0.0044,  0.0005),
"MyDs+_ds-"             : 0.5 * ufloat(0.0044,  0.0005),

"MyDs-_d+"              : ufloat(0.00028, 0.00005),
"MyDs+_d*-"             : ufloat(0.00039, 0.00008),

"ds+* MyDs-"            : 0.5 * ufloat(0.0139,0.0017),
"MyDs+* ds-"            : 0.5 * ufloat(0.0139,0.0017),

"ds*- MyDs*+"           : 0.5 * ufloat(0.0144, 0.0021),
"MyDs*- ds*+"           : 0.5 * ufloat(0.0144, 0.0021), 

# these decays are not measured yet (not in PDG) and we take them from evtgen DEC
"MyDs2457-_mu+_nu"        : ufloat(0.0040, 0),
"MyDs2317-_mu+_nu"        : ufloat(0.0040, 0),

"MyDs2457-_tau+_nu"       : ufloat(0.0018, 0), #force tau?
"MyDs2317-_tau+_nu"       : ufloat(0.0018, 0), #force tau?

"MyDs+_d-_anti_k0"        : ufloat(0.0096, 0),
"MyDs+_d0_k-"             : ufloat(0.0096, 0),
"MyDs*+_d-_anti_k0"       : ufloat(0.0096, 0),
"MyDs*+_anti_d0_k-"       : ufloat(0.0096, 0),

"MyDs+_d-_pi0_anti-k0"      : ufloat(0.0024, 0),
"MyDs+_anti_d0_pi-_anti_k0" : ufloat(0.0048, 0),
"MyDs+_d-_pi+_k-"           : ufloat(0.0048, 0),
"MyDs+_anti_d0_pi0_k-"      : ufloat(0.0024, 0),


"MyDs*+_d-_pi0_anti_k0"     : ufloat(0.0024, 0),
"MyDs*+_anti_d0_pi-_anti_k0": ufloat(0.0048, 0),
"MyDs*+_d-_pi+_k-"          : ufloat(0.0048, 0),
"MyDs*+_anti_d0_pi0_k-"     : ufloat(0.0024, 0),


"MyDs*-_d*0_k+"            : ufloat(0.0150, 0),
"MyDs*-_d*+_k0"            : ufloat(0.0150, 0),
"MyDs*-_d0_k+"             : ufloat(0.0050, 0),
"MyDs*-_d+_k0"             : ufloat(0.0050, 0),

"MyDs-_d*0_k+"             : ufloat(0.0050, 0),
"MyDs-_d*+_k0"             : ufloat(0.0050, 0),
"MyDs-_d0_k+"              : ufloat(0.0020, 0),
"MyDs-_d+_k0"              : ufloat(0.0020, 0),

"MyDs*-_d*0_k*+"           : ufloat(0.0030, 0),
"MyDs*-_d*+_k*0"           : ufloat(0.0030, 0),
"MyDs*-_d0_k*+"            : ufloat(0.0050, 0),
"MyDs*-_d+_k*0"            : ufloat(0.0050, 0),

"MyDs-_d*0_k*+"            : ufloat(0.0025, 0),
"MyDs-_d*+_k*0"            : ufloat(0.0025, 0),
"MyDs-_d0_k*+"             : ufloat(0.0025, 0),
"MyDs-_d+_k*0"             : ufloat(0.0025, 0),




} 

decays_b0 = {

"MyDs+_d-"          : ufloat(0.0072, 0.0008),
"d*-_MyDs+"         : ufloat(0.0080, 0.0011),

"MyDs*+_d-"         : ufloat(0.0074, 0.0016),
"MyDs*+_d*-"        : ufloat(0.0177, 0.0014),

"ds-_MyDs+"         : 0.5 * ufloat(0.000036, 0), #upper limit only, new in pdg, in Dec: 0.000020000 
"MyDs-_ds+"         : 0.5 * ufloat(0.000036, 0), #upper limit only, new in pdg, in Dec: 0.000020000

"ds*-_MyDs+"        : 0.5 * ufloat(0.00013, 0), #upper limit only, in Dec: 0.000024000 
"MyDs*-_ds+"        : 0.5 * ufloat(0.00013, 0), #upper limit only, in Dec: 0.000024000 

"ds*+_MyDs*-"       : 0.5 * ufloat(0.00024, 0), #upper limit only, in Dec: 0.000030000
"MyDs*+_ds*-"       : 0.5 * ufloat(0.00024, 0), #upper limit only, in Dec: 0.000030000

"MyDs2317+_d-"      : ufloat(0.00106, 0.00016),
"d*-_MyDs2317+"     : ufloat(0.0015 , 0.0006), 
"MyDs2457+_d-"      : ufloat(0.0035 , 0.0011), 
"MyDs2457+_d*-"     : ufloat(0.0093 , 0.0022), 

# these decays are not measured yet (not in PDG) and we take them from evtgen DEC
"d'1-_MyDs+"        : ufloat(0.0006, 0),  
"d'1-_MyDs*+"       : ufloat(0.0012, 0),  
"d1-_MyDs+"         : ufloat(0.0012, 0),  
"d1-_MyDs*+"        : ufloat(0.0024, 0),  
"d2*-_MyDs+"        : ufloat(0.0042, 0),  
"d2*-_MyDs*+"       : ufloat(0.0040, 0),  

"MyDs+_d-_pi0"          : ufloat(0.0018, 0),  
"MyDs+_anti_d0_pi-"     : ufloat(0.0037, 0),  
"MyDs*+_d-_pi0"         : ufloat(0.0018, 0),  
"MyDs*+_anti_d0_pi-"    : ufloat(0.0037, 0),  
"MyDs+_d-_pi-_pi+"      : ufloat(0.0030, 0),  
"MyDs+_d-_pi0_pi0"      : ufloat(0.0022, 0),  
"MyDs+_anti_d0_pi-_pi0" : ufloat(0.0022, 0),  
"MyDs*+_d-_pi-_pi+"     : ufloat(0.0030, 0),  
"MyDs*+_d-_pi0_pi0"     : ufloat(0.0022, 0),  
"MyDs*+_anti_d0_pi-_pi0": ufloat(0.0022, 0),  

}

decays_bplus = {

"MyDs-_k+_mu+_nu"     : ufloat(0.00030, 0.00014), 
#"MyDs-_k+_tau+_nu"    : ufloat(0.00030, 0.00014) # stop! this is only measured for l = e, mu
#cannot simply multiply with rDs, since the feynman diagram involves extra quarks! 
"MyDs+_anti_d0"       : ufloat(0.0090 , 0.0009 ), 
"anti_d*0_MyDs+"      : ufloat(0.0082 , 0.0017 ), 

"MyDs*-_k+_mu+_nu"    : ufloat(0.00029, 0.00019), 
#"MyDs*-_k+_tau+_nu"   : ufloat(0.00029, 0.00019) # stop! this is only measured for l = e, mu
#cannot simply multiply with rDs, since the feynman diagram involves extra quarks! 
"MyDs2317+_anti_d0"   : ufloat(0.0008 , 0.00016), 
"anti_d*0_MyDs*2317+" : ufloat(0.0009 , 0.0007 ), 
"MyDs2457+_anti_d0"   : ufloat(0.0031 , 0.0010 ), 
"anti_d*0_MyDs*2457+" : ufloat(0.0120 , 0.003  ), 
"MyDs*+_anti_d0"      : ufloat(0.0076 , 0.0016 ), 
"MyDs*+_anti_d*0"     : ufloat(0.0171 , 0.0024 ), 


# these decays are not measured yet (not in PDG) and we take them from evtgen DEC
"anti_d'10_MyDs+"         : ufloat(0.0006, 0),  
"anti_d'10_MyDs*+"        : ufloat(0.0012, 0),  
"anti_d10_MyDs+"          : ufloat(0.0012, 0),  
"anti_d10_MyDs*+"         : ufloat(0.0024, 0),  
"anti_d2*0_MyDs+"         : ufloat(0.0042, 0),  
"anti_d2*0_MyDs*+"        : ufloat(0.0040, 0),  

"MyDs+_d-_pi+"            : ufloat(0.0036, 0),  
"MyDs+_anti_d0_pi0"       : ufloat(0.0018, 0),  
"MyDs*+_d-_pi+"           : ufloat(0.0037, 0),  
"MyDs*+_anti_d0_pi0"      : ufloat(0.0018, 0),  
"MyDs+_d-_pi+_pi0"        : ufloat(0.0033, 0),  
"MyDs+_anti_d0_pi+_pi-"   : ufloat(0.0033, 0),  
"MyDs+_anti_d0_pi0_pi0"   : ufloat(0.0008, 0),  
"MyDs*+_d-_pi+_pi0"       : ufloat(0.0033, 0),  
"MyDs*+_anti_d0_pi+_pi-"  : ufloat(0.0033, 0),  
"MyDs*+_anti_d0_pi0_pi0"  : ufloat(0.0008, 0),  

#"X         anti-D'_10         MyDs*(2457)+   SVV_HELAMP 1.0 0.0 1.0 0.0 1.0 0.0;",
#"X         anti-D_10          MyDs*(2317)+   SVS;",
#"X         anti-D_10          MyDs*(2457)+   SVV_HELAMP 1.0 0.0 1.0 0.0 1.0 0.0;",
#"X         anti-D_2*0         MyDs*(2317)+   STS;",
#"X         anti-D_2*0         MyDs*(2457)+   PHSP;",

}

decays_lambdab = {

#already taken from DEC file

"lambdac+_MyDs-"  : ufloat(0.02200, 0.0),
"lambdac+_MyDs*-" : ufloat(0.04400, 0.0),   

}

decays_bcplus = {

"MyDs+_anti_d0"   : ufloat(0.00072, 0.0), #upper limit only,   in Dec: 0.000004800  
"MyDs+_d0"        : ufloat(0.00030, 0.0), #upper limit only,   in Dec: 0.000006600
"MyDs+_anti_d*0"  : ufloat(0.00046, 0.0), #upper limit only,   in Dec: 0.000007100    
"MyDs+_d*0"       : ufloat(0.00066, 0.0), #upper limit only,   in Dec: 0.000006300   

"MyDs*+_anti_d0"  : ufloat(0.00053, 0.0), #upper limit only, in Dec: 0.000004500 
"MyDs*+_d0"       : ufloat(0.0009 , 0.0), #upper limit only, in Dec: 0.000008500 
"MyDs*+_anti_d*0" : ufloat(0.0013 , 0.0), #upper limit only, in Dec: 0.000026000 
"MyDs*+_d*0"      : ufloat(0.0013 , 0.0), #upper limit only, in Dec: 0.000040400

# these decays are not measured yet (not in PDG) and we take them from evtgen DEC
# dont need them, we dont care where the Bs is coming from!

#"bs0_mu+_nu"      : ufloat(0.040300000, 0 ), 
#"bs*0_mu+_nu"     : ufloat(0.050600000, 0 ), 
#
#"b0_mu+_nu"       : ufloat(0.003400000, 0 ), 
#"b*0_mu+_nu"      : ufloat(0.005800000, 0 ), 

#"bs0_pi+"         : ufloat(0.164000000, 0 ), 
#"bs0_rho+"        : ufloat(0.072000000, 0 ), 
#"bs0_k+"          : ufloat(0.010600000, 0 ), 
#"bs0_k*+"         : ufloat(0.000000000, 0 ), 
#"bs*0_pi+"        : ufloat(0.065000000, 0 ), 
#"bs*0_rho+"       : ufloat(0.202000000, 0 ), 
#"bs*0_k+"         : ufloat(0.003700000, 0 ), 
#"bs*0_k*+"        : ufloat(0.000000000, 0 ), 



}

print_br(decays_sig,      "signals"      )
print_br(decays_bs ,      "bs background")
print_br(decays_b0 ,      "b0 background")
print_br(decays_bplus ,   "b+ background")
print_br(decays_bcplus ,  "bc background")
print_br(decays_lambdab , "Lambda background")



