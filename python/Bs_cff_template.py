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

    #untracked parameters are not saved in the output file 
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

'Decay Mytau+',  # original BR = 0.1739
'1.00000000 mu+ nu_mu anti-nu_tau PHOTOS TAULNUNU;',
'Enddecay',
'CDecay Mytau-',

'Decay MyPhi',  # original BR = 0.491
'1.00000000 K+ K- VSS;',
'Enddecay',

'Decay MyDs+',  # original BR = 0.045
'1.00000000 MyPhi pi+ SVS;',
'Enddecay',
'CDecay MyDs-',

'Decay MyDs*-', # sums up to 0.994+/-0.005 
'0.936       MyDs-    gamma   PHOTOS VSP_PWAVE;',
'0.0577      MyDs-    pi0     PHOTOS VSS;',
'Enddecay',
'CDecay MyDs*+',

#Ds*(2317) decay, compare with LHCb:
#https://gitlab.cern.ch/lhcb-datapkg/Gen/DecFiles/-/blob/master/dkfiles/B+_DstXc,Xc2hhhNneutrals_cocktail_3pi,upto5prongs=DecProdCut.dec?ref_type=heads

'Decay MyDs*(2317)-', #orignal BR is also 100% in PDG (with large unc. but ok) and in .DEC
'1.00000000 MyDs- pi0 PHSP; ',
'Enddecay',
'CDecay MyDs*(2317)+',

#Ds*(2457) decay, compare with LHCb:
#https://gitlab.cern.ch/lhcb-datapkg/Gen/DecFiles/-/blob/master/dkfiles/B+_DstXc,Xc2hhhNneutrals_cocktail_3pi,upto5prongs=DecProdCut.dec?ref_type=heads


# - MyDs*- gamma not present in the LHCb file, but it is in PDG, so we include it.
#   Its mode is motivated from MyDs*- gamma decay (Line 6687 in DECAY_NOLONGLFIE_2020.DEC)
# - LHCb is including the Ds pi0 pi0 final state, we take it over 

'Decay MyDs*(2457)+', #original BR = 0.74  
'0.18           MyDs+          gamma           VSP_PWAVE;',
'0.48           MyDs*+         pi0             PHSP;',
'0.043          MyDs+          pi+     pi-     PHSP;',
'0.037          MyDs*(2317)+   gamma           VSP_PWAVE;',
'0.022          MyDs+          pi0     pi0     PHSP;',
'Enddecay',
'CDecay MyDs*(2457)-',

# - Remark: we symmetrize all decays with more than one signal by once forcing one Ds(resonance), 
#   and then the other Ds(resonance), by dividing all BRs by a factor of 0.5 

'Decay MyBs',

## From PDG

'0.0022 MyDs- D_s+ PHSP;',  #0.0044*0.5 = 0.0022
'0.0022 D_s- MyDs+ PHSP;',  #0.0044*0.5 = 0.0022

'0.00028 MyDs- D+ PHSP;', 
'0.00039 D*- MyDs+ SVS;', 

'0.0035 MyDs*+ D_s- SVS;', #0.00695*0.5 = 0.003475
'0.0035 D_s*+ MyDs- SVS;', #0.00695*0.5 = 0.003475

'0.0072 MyDs*- D_s*+ SVV_HELAMP 1.0 0.0 1.0 0.0 1.0 0.0;', #0.0144*0.5 = 0.0072 
'0.0072 D_s*- MyDs*+ SVV_HELAMP 1.0 0.0 1.0 0.0 1.0 0.0;', #0.0144*0.5 = 0.0072

# these decays are not measured yet (not in PDG) and we take them from evtgen DEC
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
             'SoftQCD:nonDiffractive = on', # minimum bias component 
             'PTFilter:filter = on',        # this turn on the filter
             'PTFilter:quarkToFilter = 5',  # PDG id of q quark 
             'PTFilter:scaleToFilter = 3.0', 
             '531:m0 = 5.36693',            # pdg mass of Bs meson, pdg 2025
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
    ParticleID = cms.untracked.vint32(531, -531) # we need to explicitly list also cc mode, I checked.
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
     MotherIDs       = cms.untracked.vint32 (531), # Bs #charge irrelevant
     ParticleID      = cms.untracked.int32  (431)  # Ds #charge irrelevant
 )


# Logic: filter starts loops over all gen particles, and loops over ID's in particleID1. If there is a matching
# gen particle (checking the absolute ID), it loops over 

DsMuMaxMassFilter = cms.EDFilter(
     "MCParticlePairFilter",
     ParticleID1    = cms.untracked.vint32(431), # Ds, #charge irrelevant
     ParticleID2    = cms.untracked.vint32(13),  # mu  #charge irrelevant
     ParticleCharge = cms.untracked.int32 (0),   # no charge relation required for Hb 
     MaxInvMass     = cms.untracked.double(8.),
     MinPt          = cms.untracked.vdouble(-1., 6.5), #trigger is at 7, allow some space
     MinEta         = cms.untracked.vdouble(-1.e9, -1.55), #1.55 because trigger is at 1.5 (for mu) and no restrictions on Ds, bc intermediate particle 
     MaxEta         = cms.untracked.vdouble( 1.e9,  1.55),
     Status         = cms.untracked.vint32(2, 1),
)


ProductionFilterSequence = cms.Sequence(generator + motherFilter + PhiToKKFromDsFilter + DsToPhiPiFilter + DsMuMaxMassFilter)
































































































































































