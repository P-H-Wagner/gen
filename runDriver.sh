

# signals
cmsDriver.py rds/gen/python/signals_cff_template.py.py --fileout file:signals_test.root --mc --eventcontent RAWSIM --datatier GEN --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN --geometry DB:Extended --era Run2_2018 --python_filename cfgs/signals_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1

# Bs 
cmsDriver.py rds/gen/python/Bs_cff_template.py.py --fileout file:Bs_test.root --mc --eventcontent RAWSIM --datatier GEN --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN --geometry DB:Extended --era Run2_2018 --python_filename cfgs/Bs_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1

# B0
cmsDriver.py rds/gen/python/B0_cff_template.py.py --fileout file:B0_test.root --mc --eventcontent RAWSIM --datatier GEN --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN --geometry DB:Extended --era Run2_2018 --python_filename cfgs/B0_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1

# B+
cmsDriver.py rds/gen/python/B+_cff_template.py.py --fileout file:B+_test.root --mc --eventcontent RAWSIM --datatier GEN --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN --geometry DB:Extended --era Run2_2018 --python_filename cfgs/B+_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1

# Bc+
cmsDriver.py rds/gen/python/Bc+_cff_template.py.py --fileout file:Bc+_test.root --mc --eventcontent RAWSIM --datatier GEN --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN --geometry DB:Extended --era Run2_2018 --python_filename cfgs/Bc+_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1

# LambdaB
cmsDriver.py rds/gen/python/LambdaB_cff_template.py.py --fileout file:LambdaB_test.root --mc --eventcontent RAWSIM --datatier GEN --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN --geometry DB:Extended --era Run2_2018 --python_filename cfgs/LambdaB_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1
