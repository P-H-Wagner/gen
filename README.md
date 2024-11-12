# MC Production

## Get CMSSW release

Setup a CMSSW area and folder structure:
```
cmsrel CMSSW_10_6_37
mkdir CMSSW_10_6_37/src/rds 
cd CMSSW_10_6_37/src/rds
git clone https://github.com/P-H-Wagner/gen.git
cmsenv
```

## Setup the framework

Compile by running:

```
cd $CMSSW_BASE/src/rds/gen
scram b
```
Now we have to create cfg files of the cff files, which are stored in the python subfoler. We do this by running cmsDriver.py **from the source directory of the CMSSW release**. The cff files have to be **at least two folders down with respect to the src directory**. The cmsDriver command can be found in cmsDriver.sh, make it executable and run it:

```
chmod +x cmsDriver.sh
./cmsDriver dsmu hammer
```

Proceed equivalently for the other cff files. Adapt cff file, target directory, conditions, beamspot, .. if necessary.

IMPORTANT: 
Add the following lines at the end of the generated cfg file in order to enable random seeds when dividing into different jobs:
```
from IOMC.RandomEngine.RandomServiceHelper import  RandomNumberServiceHelper
randHelper =  RandomNumberServiceHelper(process.RandomNumberGeneratorService)
randHelper.populate()
process.RandomNumberGeneratorService.saveFileName =  cms.untracked.string("RandomEngineState.log")

```
Furthermore, add:
```
process.MessageLogger.cerr.FwkReport.reportEvery = 1000 #avoids the logger being floated

process.options.numberOfThreads=cms.untracked.uint32(8) #multithreading
process.options.numberOfStreams=cms.untracked.uint32(0)
process.options.numberOfConcurrentLuminosityBlocks=cms.untracked.uint32(1)

```

And change the number of events to a HOOK, which will be replaced when running ```create_cfg_and_submitter.py```:
```
input = cms.untracked.int32(HOOK_MAX_EVENTS)
```

Now, you can f.e. submit jobs du produce dsmu signals for with cfgs from the hammer directory using
```
python create_cfg_and_submitter.py dsmu hammer
```

Alternatively, exchange all HOOKs in the cfg files to real paths, numbers etc. and run it interactively using:
```
cmsRun rds/gen/dsmu_cfg_template.py
```


