import FWCore.ParameterSet.Config as cms #always
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

#use pythia8
generator = cms.EDFilter("Pythia8HadronizerFilter",

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
      'MyBc+',
      'MyBc-',
      ),

      #remark PDG ID of Bc+ is (541), the default list is cms.vint32()
      operates_on_particles = cms.vint32(541,-541),
      convertPythiaCodes = cms.untracked.bool(False),

      user_decay_embedded = cms.vstring(

'Alias      MyBc+        B_c+',
'Alias      MyBc-        B_c-',
'ChargeConj MyBc+        MyBc-',
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
'0.936       MyDs-    gamma   PHOTOS VSP_PWAVE; #[Reconstructed PDG2011]',
'0.0577      MyDs-    pi0     PHOTOS VSS; #[Reconstructed PDG2011]',
'Enddecay',
'CDecay MyDs*+',

#BR and charges checked
# all these are upper limit in pdg, take value from dec
'Decay MyBc+ ',
'0.0000048   MyDs+ anti-D0 PHSP;',
'0.0000066   MyDs+ D0 PHSP;',
'0.0000071   anti-D*0 MyDs+ SVS;',
'0.0000063   D*0 MyDs+ SVS;',
'0.000004472 MyDs*+ anti-D0 SVS;',
'0.00000845  MyDs*+ D0 SVS;',
'0.00002584  MyDs*+ anti-D*0 SVV_HELAMP 1.0 0.0 1.0 0.0 1.0 0.0;',
'0.00004015  MyDs*+ D*0 SVV_HELAMP 1.0 0.0 1.0 0.0 1.0 0.0;',

#not in pdg
'0.0017    J/psi  D_s-       SVS;',
'0.00666   J/psi  D_s*-      SVV_HELAMP 1.0 0.0 1.0 0.0 1.0 0.0;',

'Enddecay ',
'CDecay MyBc-',

 
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
             #'SoftQCD:nonDiffractive = on', # not needed for Bc (LHE origin)
             #'PTFilter:filter = on', #not needed for Bc (LHE origin)
             #'PTFilter:quarkToFilter = 5', # not needed for Bc (LHE origin)
             #'PTFilter:scaleToFilter = 3.0', #not needed for Bc (LHE origin) 
             '541:m0 = 6.27447',#pdg mass of Bc+ meson
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

# if event does not contain Bs, throw it away!
motherFilter = cms.EDFilter("MCSingleParticleFilter",
    MaxEta = cms.untracked.vdouble(2.55  , 2.55 ),
    Status = cms.untracked.vint32 (2     , 2    ), #Bs is not stable
    MinEta = cms.untracked.vdouble(-2.55 , -2.55),
    MinPt = cms.untracked.vdouble (0.0   , 0.0  ),
    ParticleID = cms.untracked.vint32(541, -541) # we need to explicitly list also cc mode, I checked.
)


# Logic: filter starts with paticle of particleID (here 333), checks if it passes all the cuts,
# then it loops over all mother ID's (here 431), and checks if particleID is an ancestor of motherID. 
# For this whole process, it considers only the ABS |.| of the pdg ID, so signs for ParticleID and motherIDs
# dont matter! Now it proceeds with finding the daughters. It loops over all daughters of the particleID
# and compares if the particle with particleID has daughters given in daugherID. 

# Important remark: While overall charge conjugation is automatically included, i.e. for particleID, motherID and 
# DaughterIDs, the relative charges within the DaugherIDs are important! Example: You want to filter for:
# Lambda -> p+ pi-, then the DaughterIDs must be given as [+2212, -211] OR [-2212, +211]
# This will then correctly pass decays of Lambda and anti-Lambda into p+ pi- and p- pi+ (I checked). However, if you give
# [+2212, +211] OR [-2212, -211], the signal (Lambda -> p+ pi^-  and aanti-Lambda -> p- pi+) will not pass!

# This is problematic for particles which are its own antiparticle! F.e. phi = 333. The state -333 does not exist.
# But the logic of the filter looks for a -333 particle in the cc case. In this case, pass -333 as daughterID

PhiToKKFromDsFilter = cms.EDFilter(
     "PythiaFilterMultiAncestor",
     DaughterIDs     = cms.untracked.vint32 ( -321,   321), # K-, K+ # relative charge is relevant!
     DaughterMaxEtas = cms.untracked.vdouble( 2.55,  2.55), # allow full eta 
     DaughterMaxPts  = cms.untracked.vdouble( 1.e9,  1.e9), # allow full pt
     DaughterMinEtas = cms.untracked.vdouble(-2.55, -2.55), # dito
     DaughterMinPts  = cms.untracked.vdouble(  0.5,   0.5), # below 0.5 bgk >> sig -> we checked
     MaxEta          = cms.untracked.double ( 99.0), # apply to the Phi, no restrictions on phi, as it is intermediate
     MinEta          = cms.untracked.double (-99.0), # apply to the Phi, dito (below it is even 1e9, no difference)
     MinPt           = cms.untracked.double (-1.0),  # apply to the Phi, dito (-1 means allow all)
     MotherIDs       = cms.untracked.vint32 (431),   # Ds  #charge irrelevant
     ParticleID      = cms.untracked.int32  (333)    # Phi #charge irrelevant
)

DsToPhiPiFilter = cms.EDFilter(
     "PythiaFilterMultiAncestor",
     #pass "anti phi" (-333) due to technitalities (see above)
     DaughterIDs     = cms.untracked.vint32 (  333,  -333,  -211), # phi, pion #relevant charge is relevant! 
     DaughterMaxEtas = cms.untracked.vdouble( 2.55,  2.55,  2.55),
     DaughterMaxPts  = cms.untracked.vdouble( 1.e9,  1.e9,  1.e9),
     DaughterMinEtas = cms.untracked.vdouble(-2.55, -2.55, -2.55),
     DaughterMinPts  = cms.untracked.vdouble(  0.5,   0.5,   0.5),
     MaxEta          = cms.untracked.double ( 99.0), #applied to the Ds
     MinEta          = cms.untracked.double (-99.0), #applied to the Ds
     MinPt           = cms.untracked.double (-1.0) , #applied to the Ds
     MotherIDs       = cms.untracked.vint32 (541), # Bs #charge irrelevant
     ParticleID      = cms.untracked.int32  (431)  # Ds #charge irrelevant
 )


# Logic: filter starts loops over all gen particles, and loops over ID's in particleID1. If there is a matching
# gen particle (checking the absolute ID), it loops over 

DsMuMaxMassFilter = cms.EDFilter(
     "MCParticlePairFilter",
     ParticleID1    = cms.untracked.vint32(431), # Ds, #charge irrelevant
     ParticleID2    = cms.untracked.vint32(13),  # mu  #charge irrelevant
     ParticleCharge = cms.untracked.int32 (0),   # no charge relation for Hb 
     MaxInvMass     = cms.untracked.double(8.),
     MinPt          = cms.untracked.vdouble(-1., 6.5), #trigger is at 7, allow some space
     MinEta         = cms.untracked.vdouble(-1.e9, -1.55), #1.55 because trigger is at 1.5 (for mu) and no restrictions on Ds, bc intermediate particle 
     MaxEta         = cms.untracked.vdouble( 1.e9,  1.55),
     Status         = cms.untracked.vint32(2, 1),
)


ProductionFilterSequence = cms.Sequence(generator + motherFilter + PhiToKKFromDsFilter + DsToPhiPiFilter + DsMuMaxMassFilter)
















