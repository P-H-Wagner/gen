# MC Production

## Get CMSSW release

Setup a CMSSW area and folder structure:
```
cmsrel CMSSW_10_6_37
mkdir CMSSW_10_6_37/src/mc 
cd CMSSW_10_6_37/src/mc
git clone https://github.com/P-H-Wagner/gen.git
cmsenv
```

Compile by running:

```
cd $CMSSW_BASE/src/mc/gen
scram b
```
Now we have to create cfg files of the cff files, which are stored in the python subfoler. We do this by running cmsDriver.py **from the source directory of the CMSSW release**. The cff files have to be **at least two folders down with respect to the src directory**:

```
cd $CMSSW_BASE/src
cmsDriver.py mc/gen/python/B+_cff_template.py \
--fileout file:i mc/gen/B+_mc_production.root \
--mc \
--eventcontent RAWSIM \
--datatier GEN \
--conditions 106X_upgrade2018_realistic_v11_L1v1 \
--beamspot Realistic25ns13TeVEarly2018Collision \
--step GEN \
--geometry DB:Extended \
--era Run2_2018 \
--python_filename mc/gen/B+_cfg_template.py \
--no_exec \
--customise Configuration/DataProcessing/Utils.addMonitoring \
-n -1
```

Proceed equivalently for the other cff files. Adapt conditions, beamspot, .. if necessary.

The cfg file which has been create with the cmsDriver command can now be run using:

```
cmsRun mc/gen/B+_cfg_template.py
```
