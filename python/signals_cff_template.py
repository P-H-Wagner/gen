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
      'MyBs',
      'Myanti-Bs',
      ),

      #remark PDG ID of Bs is (531), the default list is cms.vint32()
      operates_on_particles = cms.vint32(531,-531),
      convertPythiaCodes = cms.untracked.bool(False),

      user_decay_embedded = cms.vstring(

'Alias      MyBs       B_s0',
'Alias      Myanti-Bs  anti-B_s0',
'ChargeConj MyBs       Myanti-Bs',
'Alias      MyDs+      D_s+',
'Alias      MyDs-      D_s-',
'ChargeConj MyDs+      MyDs-',
'Alias      MyDs*+     D_s*+',
'Alias      MyDs*-     D_s*-',
'ChargeConj MyDs*+     MyDs*-',
'Alias      MyPhi      phi',
'ChargeConj MyPhi      MyPhi',
'Alias      Mytau+     tau+',
'Alias      Mytau-     tau-',
'ChargeConj Mytau-     Mytau+',

'Decay Mytau+',  # original BR = 0.1739 (pdg 2025)
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

'Decay MyDs*-', #sum of BR is 0.994 
'0.936       MyDs-    gamma    PHOTOS VSP_PWAVE;',
'0.0577      MyDs-    pi0      PHOTOS VSS;',
'Enddecay',
'CDecay MyDs*+',

# Signals,
# We set R = R* = 1, thus we directly take the same BR for tau and mu and additionnally 
# correct for the tau forcing (0.1739) and Ds* forcing (0.994) 

# Take also ISGW2 for mu signals in order to avoid difficulties with Hammer library.
'Decay MyBs',
'0.0229           MyDs-      mu+      nu_mu       PHOTOS ISGW2;', # HQET2 1.17 1.074;',
'0.05169          MyDs*-     mu+      nu_mu       PHOTOS ISGW2;', # HQET2 1.16 0.921 1.37 0.845;',
'0.00398          MyDs-      Mytau+   nu_tau      PHOTOS ISGW2;', 
'0.00899          MyDs*-     Mytau+   nu_tau      PHOTOS ISGW2;',
'Enddecay',
'CDecay Myanti-Bs',

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
             'SoftQCD:nonDiffractive = on',  # minimum bias component 
             'PTFilter:filter = on',         # this turns on the filter
             'PTFilter:quarkToFilter = 5',   # PDG id of q quark 
             'PTFilter:scaleToFilter = 3.0', # scale (checked)
             '531:m0 = 5.36691',             # mass of Bs meson, pdg 2025
              ),
         parameterSets = cms.vstring(
             'pythia8CommonSettings',
             'pythia8CP5Settings',
             'processParameters',
     ),
   ),
)

#Filter for Bs
motherFilter = cms.EDFilter("MCSingleParticleFilter",
    MaxEta = cms.untracked.vdouble(1.e9  , 1.e9 ), 
    Status = cms.untracked.vint32 (2     , 2    ), #Bs is not stable
    MinEta = cms.untracked.vdouble(-1.e9 , -1.e9),
    MinPt = cms.untracked.vdouble (0.0   , 0.0  ),
    ParticleID = cms.untracked.vint32(531, -531 ) # we need to explicitly list also cc mode, I checked.
)


#Filter for Ds -> Pi with Ds from b quark
PiFromDs             = cms.EDFilter("PythiaFilterMultiAncestor",
     # pion selection (final state particle, adapt eta and pt)
     DaughterIDs     = cms.untracked.vint32 (211),
     DaughterMaxEtas = cms.untracked.vdouble(2.55),
     DaughterMaxPts  = cms.untracked.vdouble(1.e9),
     DaughterMinEtas = cms.untracked.vdouble(-2.55),
     DaughterMinPts  = cms.untracked.vdouble(0.5),
     # ds selection (intermediate resonance)
     ParticleID      = cms.untracked.int32  (431),
     MaxEta          = cms.untracked.double (1.e9),
     MinEta          = cms.untracked.double (-1.e9),
     MinPt           = cms.untracked.double (0.0),
     # mom of ds is a b quark
     MotherIDs       = cms.untracked.vint32 (5),
)


#Filter for Ds -> Phi with Ds from b quark
PhiFromDs           = cms.EDFilter("PythiaFilterMultiAncestor",
     # phi selection (intermediate resonance)
     DaughterIDs     = cms.untracked.vint32 (333),
     DaughterMaxEtas = cms.untracked.vdouble(1.e9),
     DaughterMaxPts  = cms.untracked.vdouble(1.e9),
     DaughterMinEtas = cms.untracked.vdouble(-1.e9),
     DaughterMinPts  = cms.untracked.vdouble(0.0),
     # ds selection (intermediate resonance)
     ParticleID      = cms.untracked.int32  (431),
     MaxEta          = cms.untracked.double (1.e9),
     MinEta          = cms.untracked.double (-1.e9),
     MinPt           = cms.untracked.double (0.0),
     # mom of ds is a b quark
     MotherIDs       = cms.untracked.vint32 (5),
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
    MinPt           = cms.untracked.double (0.0),   #for the phi
    MotherIDs       = cms.untracked.vint32 (431), # Ds+
    ParticleID      = cms.untracked.int32  (333) # phi
)

#Filter for max mass of Ds + mu
DsMuMaxMassFilter = cms.EDFilter(
    "MCParticlePairFilter",
    ParticleID1    = cms.untracked.vint32(431), # Ds+
    ParticleID2    = cms.untracked.vint32(13),  # mu
    ParticleCharge = cms.untracked.int32(-1),   # opposite charge
    MaxInvMass     = cms.untracked.double(8.),
    MinPt          = cms.untracked.vdouble(-1., 6.8),     # cut on mu pt due to HLT
    MinEta         = cms.untracked.vdouble(-1.e9, -1.55), # cut on mu eta due to HLT
    MaxEta         = cms.untracked.vdouble( 1.e9,  1.55), # "
    Status         = cms.untracked.vint32(2, 1),
)

#total sequence
ProductionFilterSequence = cms.Sequence(generator + motherFilter + PiFromDs + PhiFromDs + PhiToKKFromDsFilter + DsMuMaxMassFilter)












