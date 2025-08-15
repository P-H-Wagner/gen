
export eventcontent=$1
export datatier=$2
export step=$3

echo "Running cmsDriver with eventcontent: $eventcontent"
echo "Running cmsDriver with datatier: $datatier"
echo "Running cmsDriver with step: $step"

#example
#./runDriver_privateHbProd.sh RAWSIM GEN-SIM GEN,SIM

#path to save the cfg
path=/work/pahwagne/gen/CMSSW_10_6_37/src/rds/gen/$datatier
mkdir -p $path/hb/
mkdir -p $path/signals/


echo "cmsDriver.py rds/gen/python/hb_cff_template.py --fileout file:hb_test.root --mc --eventcontent $eventcontent --datatier $datatier --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step $step --geometry DB:Extended --era Run2_2018 --python_filename $path/hb/hb_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1"

# signals
cmsDriver.py rds/gen/python/hb_cff_template.py --fileout file:hb_test.root --mc --eventcontent $eventcontent --datatier $datatier --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step $step --geometry DB:Extended --era Run2_2018 --python_filename $path/hb/hb_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1 --customise_commands 'process.RandomNumberGeneratorService.generator.initialSeed = 12345'

echo "cmsDriver.py rds/gen/python/signals_cff_template.py --fileout file:signals_test.root --mc --eventcontent $eventcontent --datatier $datatier --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step $step --geometry DB:Extended --era Run2_2018 --python_filename $path/signals/signals_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1"

cmsDriver.py rds/gen/python/signals_cff_template.py --fileout file:signals_test.root --mc --eventcontent $eventcontent --datatier $datatier --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step $step --geometry DB:Extended --era Run2_2018 --python_filename $path/signals/signals_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1
