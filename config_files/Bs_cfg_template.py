# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: rds/gen/python/Bs_cff_template.py.py --fileout file:Bs_test.root --mc --eventcontent RAWSIM --datatier GEN --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN --geometry DB:Extended --era Run2_2018 --python_filename cfgs/Bs_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run2_2018_cff import Run2_2018

process = cms.Process('GEN',Run2_2018)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic25ns13TeVEarly2018Collision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(HOOK_MAX_EVENTS)
)

# Dont forget me!
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# Input source
process.source = cms.Source("EmptySource", firstLuminosityBlock = cms.untracked.uint32(HOOK_FIRST_LUMI))

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('rds/gen/python/Bs_cff_template.py.py nevts:-1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    ),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(1),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(20971520),
    fileName = cms.untracked.string('file:HOOK_FILE_OUT'),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_upgrade2018_realistic_v11_L1v1', '')

process.DsToPhiPiFilter = cms.EDFilter("PythiaFilterMultiAncestor",
    DaughterIDs = cms.untracked.vint32(333, -333, -211),
    DaughterMaxEtas = cms.untracked.vdouble(2.55, 2.55, 2.55),
    DaughterMaxPts = cms.untracked.vdouble(1000000000.0, 1000000000.0, 1000000000.0),
    DaughterMinEtas = cms.untracked.vdouble(-2.55, -2.55, -2.55),
    DaughterMinPts = cms.untracked.vdouble(0.5, 0.5, 0.5),
    MaxEta = cms.untracked.double(99.0),
    MinEta = cms.untracked.double(-99.0),
    MinPt = cms.untracked.double(-1.0),
    MotherIDs = cms.untracked.vint32(531),
    ParticleID = cms.untracked.int32(431)
)


process.PhiToKKFromDsFilter = cms.EDFilter("PythiaFilterMultiAncestor",
    DaughterIDs = cms.untracked.vint32(-321, 321),
    DaughterMaxEtas = cms.untracked.vdouble(2.55, 2.55),
    DaughterMaxPts = cms.untracked.vdouble(1000000000.0, 1000000000.0),
    DaughterMinEtas = cms.untracked.vdouble(-2.55, -2.55),
    DaughterMinPts = cms.untracked.vdouble(0.5, 0.5),
    MaxEta = cms.untracked.double(99.0),
    MinEta = cms.untracked.double(-99.0),
    MinPt = cms.untracked.double(-1.0),
    MotherIDs = cms.untracked.vint32(431),
    ParticleID = cms.untracked.int32(333)
)

process.DsToPiFromBsFilter = cms.EDFilter("PythiaFilterMultiAncestor",
    DaughterIDs = cms.untracked.vint32(211),
    DaughterMaxEtas = cms.untracked.vdouble(2.55),
    DaughterMaxPts = cms.untracked.vdouble(1000000000.0),
    DaughterMinEtas = cms.untracked.vdouble(-2.55),
    DaughterMinPts = cms.untracked.vdouble(0.5),
    MaxEta = cms.untracked.double(99.0),
    MinEta = cms.untracked.double(-99.0),
    MinPt = cms.untracked.double(-1.0),
    MotherIDs = cms.untracked.vint32(531),
    ParticleID = cms.untracked.int32(431)
)

process.DsToPhiFromBsFilter = cms.EDFilter("PythiaFilterMultiAncestor",
    DaughterIDs = cms.untracked.vint32(333),
    DaughterMaxEtas = cms.untracked.vdouble(2.55),
    DaughterMaxPts = cms.untracked.vdouble(1000000000.0),
    DaughterMinEtas = cms.untracked.vdouble(-2.55),
    DaughterMinPts = cms.untracked.vdouble(0.5),
    MaxEta = cms.untracked.double(99.0),
    MinEta = cms.untracked.double(-99.0),
    MinPt = cms.untracked.double(-1.0),
    MotherIDs = cms.untracked.vint32(531),
    ParticleID = cms.untracked.int32(431)
)



process.generator = cms.EDFilter("Pythia8GeneratorFilter",
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            convertPythiaCodes = cms.untracked.bool(False),
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2020_NOLONGLIFE.DEC'),
            list_forced_decays = cms.vstring(
                'MyBs', 
                'Myanti-Bs'
            ),
            operates_on_particles = cms.vint32(531, -531),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2020.pdl'),
            user_decay_embedded = cms.vstring(
                'Alias      MyBs         B_s0', 
                'Alias      Myanti-Bs    anti-B_s0', 
                'ChargeConj Myanti-Bs    MyBs', 
                'Alias      Mytau+       tau+', 
                'Alias      Mytau-       tau-', 
                'ChargeConj Mytau-       Mytau+', 
                'Alias      MyDs+        D_s+', 
                'Alias      MyDs-        D_s-', 
                'ChargeConj MyDs-        MyDs+', 
                'Alias      MyDs*+       D_s*+', 
                'Alias      MyDs*-       D_s*-', 
                'ChargeConj MyDs*-       MyDs*+', 
                'Alias      MyPhi        phi', 
                'ChargeConj MyPhi        MyPhi', 
                'Alias      MyDs*(2317)- D_s0*- ', 
                'Alias      MyDs*(2317)+ D_s0*+ ', 
                'ChargeConj MyDs*(2317)+ MyDs*(2317)-', 
                'Alias      MyDs*(2457)- D_s1- ', 
                'Alias      MyDs*(2457)+ D_s1+ ', 
                'ChargeConj MyDs*(2457)+ MyDs*(2457)-', 
                'Decay Mytau+', 
                '1.00000000 mu+ nu_mu anti-nu_tau PHOTOS TAULNUNU;', 
                'Enddecay', 
                'CDecay Mytau-', 
                'Decay MyPhi', 
                '1.00000000 K+ K- VSS;', 
                'Enddecay', 
                'Decay MyDs+', 
                '1.00000000 MyPhi pi+ SVS;', 
                'Enddecay', 
                'CDecay MyDs-', 
                'Decay MyDs*-', 
                '0.936       MyDs-    gamma   PHOTOS VSP_PWAVE;', 
                '0.0577      MyDs-    pi0     PHOTOS VSS;', 
                'Enddecay', 
                'CDecay MyDs*+', 
                'Decay MyDs*(2317)-', 
                '1.00000000 MyDs- pi0 PHSP; ', 
                'Enddecay', 
                'CDecay MyDs*(2317)+', 
                'Decay MyDs*(2457)+', 
                '0.18           MyDs+          gamma           VSP_PWAVE;', 
                '0.48           MyDs*+         pi0             PHSP;', 
                '0.043          MyDs+          pi+     pi-     PHSP;', 
                '0.037          MyDs*(2317)+   gamma           VSP_PWAVE;', 
                '0.022          MyDs+          pi0     pi0     PHSP;', 
                'Enddecay', 
                'CDecay MyDs*(2457)-', 
                'Decay MyBs', 
                '0.0022 MyDs- D_s+ PHSP;', 
                '0.0022 D_s- MyDs+ PHSP;', 
                '0.00028 MyDs- D+ PHSP;', 
                '0.00039 D*- MyDs+ SVS;', 
                '0.0035 MyDs*+ D_s- SVS;', 
                '0.0035 D_s*+ MyDs- SVS;', 
                '0.0072 MyDs*- D_s*+ SVV_HELAMP 1.0 0.0 1.0 0.0 1.0 0.0;', 
                '0.0072 D_s*- MyDs*+ SVV_HELAMP 1.0 0.0 1.0 0.0 1.0 0.0;', 
                '0.0030     MyDs*(2457)-   mu+    nu_mu        PHOTOS       ISGW2;', 
                '0.0040     MyDs*(2317)-   mu+    nu_mu        PHOTOS       ISGW2;', 
                '0.00137    MyDs*(2457)-   tau+   nu_tau                    ISGW2;', 
                '0.0018     MyDs*(2317)-   tau+   nu_tau                    ISGW2;', 
                '0.0096     MyDs+        D-          anti-K0                PHSP;', 
                '0.0096     MyDs+        D0          K-                     PHSP;', 
                '0.00954    MyDs*+       D-          anti-K0                PHSP;', 
                '0.00954    MyDs*+       anti-D0     K-                     PHSP;', 
                '0.0024     MyDs+        D-          pi0        anti-K0     PHSP;', 
                '0.0048     MyDs+        anti-D0     pi-        anti-K0     PHSP;', 
                '0.0048     MyDs+        D-          pi+        K-          PHSP;', 
                '0.0024     MyDs+        anti-D0     pi0        K-          PHSP;', 
                '0.002385   MyDs*+       D-          pi0        anti-K0     PHSP;', 
                '0.004770   MyDs*+       anti-D0     pi-        anti-K0     PHSP;', 
                '0.004770   MyDs*+       D-          pi+        K-          PHSP;', 
                '0.002385   MyDs*+       anti-D0     pi0        K-          PHSP;', 
                '0.01491    MyDs*-       D*0         K+                     PHSP;', 
                '0.01491    MyDs*-       D*+         K0                     PHSP;', 
                '0.004968   MyDs*-       D0          K+                     PHSP;', 
                '0.004968   MyDs*-       D+          K0                     PHSP;', 
                '0.0050     MyDs-        D*0         K+                     PHSP;', 
                '0.0050     MyDs-        D*+         K0                     PHSP;', 
                '0.0020     MyDs-        D0          K+                     PHSP;', 
                '0.0020     MyDs-        D+          K0                     PHSP;', 
                '0.002981   MyDs*-       D*0         K*+                    PHSP;', 
                '0.002981   MyDs*-       D*+         K*0                    PHSP;', 
                '0.004968   MyDs*-       D0          K*+                    PHSP;', 
                '0.004968   MyDs*-       D+          K*0                    PHSP;', 
                '0.0025     MyDs-        D*0         K*+                    PHSP;', 
                '0.0025     MyDs-        D*+         K*0                    PHSP;', 
                '0.0025     MyDs-        D0          K*+                    PHSP;', 
                '0.0025     MyDs-        D+          K*0                    PHSP;', 
                '0.001689   MyDs*+       D-                                 SVS;', 
                '0.001689   MyDs*+       D*-    SVV_HELAMP  1.0 0.0 1.0 0.0 1.0 0.0;', 
                'Enddecay', 
                'CDecay Myanti-Bs', 
                'End'
            )
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        parameterSets = cms.vstring(
            'pythia8CommonSettings', 
            'pythia8CP5Settings', 
            'processParameters'
        ),
        processParameters = cms.vstring(
            'SoftQCD:nonDiffractive = on', 
            'PTFilter:filter = on', 
            'PTFilter:quarkToFilter = 5', 
            'PTFilter:scaleToFilter = 3.0', 
            '531:m0 = 5.36693'
        ),
        pythia8CP5Settings = cms.vstring(
            'Tune:pp 14', 
            'Tune:ee 7', 
            'MultipartonInteractions:ecmPow=0.03344', 
            'MultipartonInteractions:bProfile=2', 
            'MultipartonInteractions:pT0Ref=1.41', 
            'MultipartonInteractions:coreRadius=0.7634', 
            'MultipartonInteractions:coreFraction=0.63', 
            'ColourReconnection:range=5.176', 
            'SigmaTotal:zeroAXB=off', 
            'SpaceShower:alphaSorder=2', 
            'SpaceShower:alphaSvalue=0.118', 
            'SigmaProcess:alphaSvalue=0.118', 
            'SigmaProcess:alphaSorder=2', 
            'MultipartonInteractions:alphaSvalue=0.118', 
            'MultipartonInteractions:alphaSorder=2', 
            'TimeShower:alphaSorder=2', 
            'TimeShower:alphaSvalue=0.118', 
            'SigmaTotal:mode = 0', 
            'SigmaTotal:sigmaEl = 21.89', 
            'SigmaTotal:sigmaTot = 100.309', 
            'PDF:pSet=LHAPDF6:NNPDF31_nnlo_as_0118'
        ),
        pythia8CommonSettings = cms.vstring(
            'Tune:preferLHAPDF = 2', 
            'Main:timesAllowErrors = 10000', 
            'Check:epTolErr = 0.01', 
            'Beams:setProductionScalesFromLHEF = off', 
            'SLHA:keepSM = on', 
            'SLHA:minMassSM = 1000.', 
            'ParticleDecays:limitTau0 = on', 
            'ParticleDecays:tau0Max = 10', 
            'ParticleDecays:allowPhotonRadiation = on'
        )
    ),
    comEnergy = cms.double(13000.0),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    pythiaPylistVerbosity = cms.untracked.int32(0)
)


process.DsMuMaxMassFilter = cms.EDFilter("MCParticlePairFilter",
    MaxEta = cms.untracked.vdouble(1000000000.0, 1.55),
    MaxInvMass = cms.untracked.double(8.0),
    MinEta = cms.untracked.vdouble(-1000000000.0, -1.55),
    MinPt = cms.untracked.vdouble(-1.0, 6.5),
    ParticleCharge = cms.untracked.int32(0),
    ParticleID1 = cms.untracked.vint32(431),
    ParticleID2 = cms.untracked.vint32(13),
    Status = cms.untracked.vint32(2, 1)
)


process.motherFilter = cms.EDFilter("MCSingleParticleFilter",
    MaxEta = cms.untracked.vdouble(2.55, 2.55),
    MinEta = cms.untracked.vdouble(-2.55, -2.55),
    MinPt = cms.untracked.vdouble(0.0, 0.0),
    ParticleID = cms.untracked.vint32(531, -531),
    Status = cms.untracked.vint32(2, 2)
)


#process.ProductionFilterSequence = cms.Sequence(process.generator+process.motherFilter+process.PhiToKKFromDsFilter+process.DsToPhiPiFilter+process.DsMuMaxMassFilter)
#process.ProductionFilterSequence = cms.Sequence(process.generator) #+process.motherFilter+process.PhiToKKFromDsFilter+process.DsToPhiPiFilter+process.DsMuMaxMassFilter)
process.ProductionFilterSequence = cms.Sequence(process.generator+process.motherFilter+process.PhiToKKFromDsFilter+process.DsToPiFromBsFilter+process.DsToPhiFromBsFilter+process.DsMuMaxMassFilter)

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.endjob_step,process.RAWSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
process.options.numberOfThreads=cms.untracked.uint32(8)
process.options.numberOfStreams=cms.untracked.uint32(0)
process.options.numberOfConcurrentLuminosityBlocks=cms.untracked.uint32(1)




# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path).insert(0, process.ProductionFilterSequence)

# customisation of the process.

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

from IOMC.RandomEngine.RandomServiceHelper import  RandomNumberServiceHelper
randHelper =  RandomNumberServiceHelper(process.RandomNumberGeneratorService)
randHelper.populate()
process.RandomNumberGeneratorService.saveFileName =  cms.untracked.string("RandomEngineState.log")
