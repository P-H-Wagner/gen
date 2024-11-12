#!/bin/sh

#given by command line
export channel=$1  #cff naming; Bs, B0, .., dsmu, dstau, ...

#remark conditions and beamspot in this case are irrelevant because we do gen only

cmsDriver.py rds/gen/python/${channel}_cff_template.py \
--fileout file:HOOK_FILE_OUT \
--mc \
--eventcontent RAWSIM \
--datatier GEN \
--conditions 106X_upgrade2018_realistic_v11_L1v1 \
--beamspot Realistic25ns13TeVEarly2018Collision \
--step GEN \
--geometry DB:Extended \
--era Run2_2018 \
--python_filename config_files/${channel}_cfg_template.py \
--no_exec \
--customise Configuration/DataProcessing/Utils.addMonitoring \
-n -1 
