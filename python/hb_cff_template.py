import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13000.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table            = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2020_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2020.pdl'),
            list_forced_decays     = cms.vstring(
                'MyDs+',
                'MyDs-',
            ),        
            operates_on_particles = cms.vint32(431,-431), # consider forcing of Ds and Phi
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring([
                'Alias      MyDs+      D_s+',
                'Alias      MyDs-      D_s-',
                'ChargeConj MyDs+      MyDs-',

                'Alias      MyPhi      phi',
                'ChargeConj MyPhi      MyPhi',

                'Decay MyDs-',
                '  1.000    MyPhi pi-    PHOTOS SVS;',
                'Enddecay',
                'CDecay MyDs+',

                'Decay MyPhi',
                '  1.000    K+ K-        PHOTOS VSS;',
                'Enddecay',

                'End',
            ]),
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'SoftQCD:nonDiffractive = on',
            'PTFilter:filter = on', # this turns on the filter
            'PTFilter:quarkToFilter = 5', # PDG id of q quark
            'PTFilter:scaleToFilter = 3.0', #scale (checked)
            '531:m0 = 5.36691', # mass of Bs meson, pdg 2025
		),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP5Settings',
            'processParameters',
        ),
    ),
)

#Filter for Ds -> Pi
PiFromDs = cms.EDFilter("PythiaFilterMultiMother",
    ParticleID   = cms.untracked.int32  (211),
    maxetacut    = cms.untracked.vdouble(2.55), #pion is final state, must be in the eta coverage
    maxptcut     = cms.untracked.vdouble(1.e9),
    minetacut    = cms.untracked.vdouble(-2.55),
    minptcut     = cms.untracked.vdouble(0.5),
    Status       = cms.untracked.int32(1), #pion is stable
    MotherIDs    = cms.untracked.vint32(431),
)

#Filter for Ds -> Phi
PhiFromDs = cms.EDFilter("PythiaFilterMultiMother",
    ParticleID   = cms.untracked.int32  (333),
    maxetacut    = cms.untracked.vdouble(1.e9), #phi is intermediate state, we dont care about its eta, as long as the two kaons are covered
    maxptcut     = cms.untracked.vdouble(1.e9),
    minetacut    = cms.untracked.vdouble(-1.e9),
    minptcut     = cms.untracked.vdouble(0.0),
    Status       = cms.untracked.int32(2), #phi is instable
    MotherIDs    = cms.untracked.vint32(431),
)


#Filter for Phi -> KK
PhiToKKFromDsFilter = cms.EDFilter(
    "PythiaFilterMultiAncestor",
    DaughterIDs     = cms.untracked.vint32 ( -321,   321), # K-, K+
    DaughterMaxEtas = cms.untracked.vdouble( 2.55,  2.55), #kaons are final state, must be in the eta coverage
    DaughterMaxPts  = cms.untracked.vdouble( 1.e9,  1.e9),
    DaughterMinEtas = cms.untracked.vdouble(-2.55, -2.55),
    DaughterMinPts  = cms.untracked.vdouble(  0.5,   0.5),
    MaxEta          = cms.untracked.double ( 1.e9), #for the phi
    MinEta          = cms.untracked.double (-1.e9), #for the phi
    MinPt           = cms.untracked.double ( 0.0 ),  #for the phi
    MotherIDs       = cms.untracked.vint32 (431), # Ds+
    ParticleID      = cms.untracked.int32  (333) # phi
)

#Filter for max mass of Ds + mu
DsMuMaxMassFilter = cms.EDFilter(
    "MCParticlePairFilter",
    ParticleID1    = cms.untracked.vint32(431), # Ds+
    ParticleID2    = cms.untracked.vint32(13), # mu
    ParticleCharge = cms.untracked.int32(0), # opposite charge
    MaxInvMass     = cms.untracked.double(8.),
    MinPt          = cms.untracked.vdouble(-1., 7.),      # harder cut on mu pt due to HLT
    MinEta         = cms.untracked.vdouble(-1.e9, -1.55), # harder cut on mu eta due to HLT
    MaxEta         = cms.untracked.vdouble( 1.e9,  1.55), # "
    Status         = cms.untracked.vint32(2, 1),
)

#total sequence
ProductionFilterSequence = cms.Sequence(generator + PiFromDs + PhiFromDs + PhiToKKFromDsFilter + DsMuMaxMassFilter)
