import FWCore.ParameterSet.Config as cms #always
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

#use pythia8
generator = cms.EDFilter("Pythia8GeneratorFilter",

  #service parameters
  pythiaPylistVerbosity = cms.untracked.int32(0),
  pythiaHepMCVerbosity = cms.untracked.bool(False),
  maxEventsToPrint = cms.untracked.int32(0),

  #center of mass energy
  comEnergy = cms.double(13000.0),
  ExternalDecays = cms.PSet(

    #untracked parameters are not saved in the output file as they have no e    ffect on the final output files
    #and thus are not useful information to save
    EvtGen130 = cms.untracked.PSet(
      #everything which is not forced is found here (or in pythia)
      decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2020_NOLONGLIFE.DEC'),
      #masses, lifetimes, ...
      particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2020.pdl'),
      

      list_forced_decays = cms.vstring(
      'MyLambdaB',
      'Myanti-LambdaB',
      ),

      #remark PDG ID of Bs is (531), the default list is cms.vint32()
      operates_on_particles = cms.vint32(5122,-5122),
      convertPythiaCodes = cms.untracked.bool(False),

      user_decay_embedded = cms.vstring(

'Alias      MyLambdaB Lambda_b0',
'Alias      Myanti-LambdaB anti-Lambda_b0',
'ChargeConj Myanti-LambdaB MyLambdaB',
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

'Decay Mytau+',  # original BR = 0.1739
'1.00000000 mu+ nu_mu anti-nu_tau PHOTOS TAULNUNU;',
'Enddecay',
'CDecay Mytau-',

'Decay MyPhi',  # original BR = 0.489
'1.00000000 K+ K- VSS;',
'Enddecay',

'Decay MyDs+',  # original BR = 0.0221
'1.00000000 MyPhi pi+ SVS;',
'Enddecay',
'CDecay MyDs-',

'Decay MyDs*-',
'0.942      MyDs-    gamma   PHOTOS VSP_PWAVE; #[Reconstructed PDG2011]',
'0.058      MyDs-    pi0     PHOTOS VSS; #[Reconstructed PDG2011]',
'Enddecay',
'CDecay MyDs*+',

#Both decays are taken from DECAY_NOLONGLFIE_2020.DEC
#The ratios are also taken from there, they are *not* consistent with the PDG,
#however it is an overall factor of 2, which does not matter for the production.
#

#Remark that the MyDs*- mode is not in the pdg, but as otherwise we just have a single mode
#to force, and we know it is there, we take it as well. This is the only time we do this!!!
#Normally such cases are in the mother_notinPDG.dec file!

#BR and charges checked
'Decay MyLambdaB',
'0.02200    Lambda_c+       MyDs-                         PHSP;',
'0.04400    Lambda_c+       MyDs*-                        PHSP;',
'Enddecay ',
'CDecay Myanti-LambdaB',

'End',

      ),
      ),
      parameterSets = cms.vstring('EvtGen130'),
      ),

#fix some pythia parameters
     PythiaParameters = cms.PSet(
         pythia8CommonSettingsBlock,
         pythia8CP5SettingsBlock,
         processParameters = cms.vstring(
             'SoftQCD:nonDiffractive = on', #minimum bias component 
             'PTFilter:filter = on', # this turn on the filter
             'PTFilter:quarkToFilter = 5', # PDG id of q quark 
             'PTFilter:scaleToFilter = 3.0', 
             '5122:m0 = 5.61960',#pdg mass of lambdaB 
             #'ProcessLevel:all = off',
 #            'HardQCD:hardbbbar = on',
 #            'PhaseSpace:pTHatMin = 100',
              ),
         parameterSets = cms.vstring(
             'pythia8CommonSettings',
             'pythia8CP5Settings',
             'processParameters',


     ),
   ),
)

PhiToKKFromDsFilter = cms.EDFilter(
     "PythiaFilterMultiAncestor",
     DaughterIDs     = cms.untracked.vint32 ( -321,   321), # K-, K+
     DaughterMaxEtas = cms.untracked.vdouble( 2.55,  2.55), # allow full eta 
     DaughterMaxPts  = cms.untracked.vdouble( 1.e9,  1.e9), # allow full pt
     DaughterMinEtas = cms.untracked.vdouble(-2.55, -2.55), # dito
     DaughterMinPts  = cms.untracked.vdouble(  0.5,   0.5), # below 0.5 bgk >> sig -> we checked
     MaxEta          = cms.untracked.double ( 99.0), # no restrictions on phi, as it is intermediate
     MinEta          = cms.untracked.double (-99.0), # dito (below it is even 1e9, no difference)
     MinPt           = cms.untracked.double (-1.0),  # dito (-1 means allow all)
     MotherIDs       = cms.untracked.vint32 (431), # Ds+
     ParticleID      = cms.untracked.int32  (333) # phi
)

DsMuMaxMassFilter = cms.EDFilter(
     "MCParticlePairFilter",
     ParticleID1    = cms.untracked.vint32(431), # Ds+
     ParticleID2    = cms.untracked.vint32(13), # mu
     ParticleCharge = cms.untracked.int32(-1), # opposite charge
     MaxInvMass     = cms.untracked.double(8.),
     MinPt          = cms.untracked.vdouble(-1., 6.5), #trigger is at 7, allow some space
     MinEta         = cms.untracked.vdouble(-1.e9, -1.55), #1.55 because trigger is at 1.5 (for mu) and no restrictions on Ds, bc intermediate particle 
     MaxEta         = cms.untracked.vdouble( 1.e9,  1.55),
     Status         = cms.untracked.vint32(2, 1),
)


ProductionFilterSequence = cms.Sequence(generator + PhiToKKFromDsFilter + DsMuMaxMassFilter)









































































































































































