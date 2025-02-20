import numpy as np
from uncertainties import ufloat



tau_scale    = ufloat(0.1739, 0.0004)
dsStar_scale = ufloat(0.936 , 0.004 ) + ufloat(0.0577, 0.0035) 



def print_br(dictionary):

  output = dictionary.copy()

  for key in dictionary.keys():
    
    if "tau" in key: output[key] *= tau_scale
    if "ds*" in key: output[key] *= dsStar_scale

  max_key_length = max(len(key) for key in output)

  for key, value in output.items():
    print(f"{key:<{max_key_length}}: {value}")



#define dict for each mom
decays_sig =  {

"ds_mu_nu"   : ufloat(0.0231 , 0.0021 ),
"ds*_mu_nu"  : ufloat(0.052  , 0.005  ),
"ds_tau_nu"  : ufloat(0.0231 , 0.0021 ), # since r  = 1
"ds*_tau_nu" : ufloat(0.052  , 0.005  ), # since r* = 1

}


decays_bs = {

"ds_ds"                 : 0.5 * ufloat(0.0044,  0.0005),
"ds_ds"                 : 0.5 * ufloat(0.0044,  0.0005),

"ds_d"                  : ufloat(0.00028, 0.00005),
"ds_dStar"              : ufloat(0.00039, 0.00008),

"dsStar ds"             : 0.5 * ufloat(0.0139,0.0017),
"dsStar ds"             : 0.5 * ufloat(0.0139,0.0017),

"dsStar dsStar"         : 0.5 * ufloat(0.0144, 0.0021),
"dsStar dsStar"         : 0.5 * ufloat(0.0144, 0.0021), 

# these decays are not measured yet (not in PDG) and we take them from evtgen DEC
"ds2457_mu_nu"          : ufloat(0.0040, 0),
"ds2317_mu_nu"          : ufloat(0.0040, 0),

"ds2457_tau_nu"         : ufloat(0.0018, 0),
"ds2317_tau_nu"         : ufloat(0.0018, 0),

"ds_d_K"                : ufloat(0.0096, 0),
"ds_d_k"                : ufloat(0.0096, 0),
"dsStar_d_K"            : ufloat(0.0096, 0),
"dsStar_D_K"            : ufloat(0.0096, 0),

"ds_d_pi_K"             : ufloat(0.0024, 0),
"ds_D_pi_K"             : ufloat(0.0048, 0),
"ds_d_pi_k"             : ufloat(0.0048, 0),
"ds_D_pi_k"             : ufloat(0.0024, 0),


"dsStar_d_pi_K"         : ufloat(0.0024, 0),
"dsStar_D_pi_K"         : ufloat(0.0048, 0),
"dsStar_d_pi_K"         : ufloat(0.0048, 0),
"dsStar_D_pi_k"         : ufloat(0.0024, 0),


"dsStar_dStar_k"        : ufloat(0.0150, 0),
"dsStar_dStar_k"        : ufloat(0.0150, 0),
"dsStar_d_k"            : ufloat(0.0050, 0),
"dsStar_d_k"            : ufloat(0.0050, 0),

"ds_dStar_k"            : ufloat(0.0050, 0),
"ds_dStar_k"            : ufloat(0.0050, 0),
"ds_d_k"                : ufloat(0.0020, 0),
"ds_d_k"                : ufloat(0.0020, 0),

"dsStar_dStar_kStar"    : ufloat(0.0030, 0),
"dsStar_dStar_kStar"    : ufloat(0.0030, 0),
"dsStar_d_kStar"        : ufloat(0.0050, 0),
"dsStar_d_kStar"        : ufloat(0.0050, 0),

"ds_dStar_kStar"        : ufloat(0.0025, 0),
"ds_dStar_kStar"        : ufloat(0.0025, 0),
"ds_d_kStar"            : ufloat(0.0025, 0),
"ds_d_kStar"            : ufloat(0.0025, 0),




} 

decays_b0 = {

"ds_d"          : ufloat(0.0072, 0),
"dStar_ds"      : ufloat(0.0080, 0),

"dsStar_d"      : ufloat(0.0074, 0),
"dsStar_dStar"  : ufloat(0.0177, 0),

"dsStar_ds"     : ufloat(0.000065, 0),
"dsStar_ds"     : ufloat(0.000065, 0),

"dsStar_dsStar" : ufloat(0.00012, 0),
"dsStar_dsStar" : ufloat(0.00012, 0),

"ds2317_d"      : ufloat(0.00106, 0),
"dStar_ds2317"  : ufloat(0.0015, 0), 
"ds2457_d"      : ufloat(0.0035, 0), 
"ds2457_dStar"  : ufloat(0.0093, 0), 



"d_ds"          : ufloat(0.0006, 0),  
"d_dsStar"      : ufloat(0.0012, 0),  
"d_ds"          : ufloat(0.0012, 0),  
"d_dsStar"      : ufloat(0.0024, 0),  
"dStar_ds"      : ufloat(0.0042, 0),  
"dStar_dsStar"  : ufloat(0.0040, 0),  

"ds_d_pi"       : ufloat(0.0018, 0),  
"ds_d_pi"       : ufloat(0.0037, 0),  
"dsStar_d_pi"   : ufloat(0.0018, 0),  
"dsStar_d_pi"   : ufloat(0.0037, 0),  
"ds_d_pi_pi"    : ufloat(0.0030, 0),  
"ds_d_pi_pi"    : ufloat(0.0022, 0),  
"ds_d_pi_pi"    : ufloat(0.0022, 0),  
"dsStar_d_pi_pi": ufloat(0.0030, 0),  
"dsStar_d_pi_pi": ufloat(0.0022, 0),  
"dsStar_d_pi_pi": ufloat(0.0022, 0),  

}


print_br(decays_sig)
print_br(decays_bs)



