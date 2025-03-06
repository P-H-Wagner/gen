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
      'MyB0',
      'Myanti-B0',
      ),

      #remark PDG ID of B0 is (511), the default list is cms.vint32()
      operates_on_particles = cms.vint32(511,-511),
      convertPythiaCodes = cms.untracked.bool(False),

      user_decay_embedded = cms.vstring(

'Alias      MyB0         B0',
'Alias      Myanti-B0    anti-B0',
'ChargeConj Myanti-B0    MyB0',

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

'Decay MyDs*-', # original BR = 0.9937
'0.936      MyDs-    gamma   PHOTOS VSP_PWAVE;',
'0.0577     MyDs-    pi0     PHOTOS VSS;',
'Enddecay',
'CDecay MyDs*+',

#Ds*(2317) decay, mode from LHCb:
#https://gitlab.cern.ch/lhcb-datapkg/Gen/DecFiles/-/blob/master/dkfiles/B+_DstXc,Xc2hhhNneutrals_cocktail_3pi,upto5prongs=DecProdC    ut.dec?ref_type=heads

'Decay MyDs*(2317)-', #orignal BR is also 100% in PDG (with large unc. but ok) and in .DEC
'1.00000000 MyDs- pi0 PHSP; ',
'Enddecay',
'CDecay MyDs*(2317)+',

#Ds*(2457) decay, mode from LHCb:
#https://gitlab.cern.ch/lhcb-datapkg/Gen/DecFiles/-/blob/master/dkfiles/B+_DstXc,Xc2hhhNneutrals_cocktail_3pi,upto5prongs=DecProdC    ut.dec?ref_type=heads


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

# - Mode for B0 -> Ds*+ Ds*- is taken from Bs -> Ds*+ Ds*-, given that both B mesons have the same spin.
# - Remark: we symmetrize all decays with more than one signal by once forcing one Ds(resonance), 
#   and then the other Ds(resonance), by dividing all BRs by a factor of 0.5 

#BR and charges checked
'Decay MyB0',

'0.0072 MyDs+ D- PHSP;',
'0.0080 D*- MyDs+ SVS; ',
'0.0074 MyDs*+ D- SVS; ',
'0.0176 MyDs*+ D*- SVV_HELAMP 0.4904 0.0 0.7204 0.0 0.4904 0.0;',

'0.00001 MyDs+  D_s-                                   PHSP;',
'0.00001 D_s+   MyDs-                                  PHSP;',

'0.00001192 MyDs*- D_s+ SVS; ', ##upper limit, take value from dec!  
'0.000012   D_s*- MyDs+ SVS; ', ##upper limit, take value from dec!  

'0.00001491 MyDs*- D_s*+ SVV_HELAMP 1.0 0.0 1.0 0.0 1.0 0.0;', #0.00024*0.5=0.00012 #upper limit and not in dec! remove? 
'0.00001491 D_s*- MyDs*+ SVV_HELAMP 1.0 0.0 1.0 0.0 1.0 0.0;', #0.00024*0.5=0.00012 #upper limit and not in dec! remove? 

'0.00106 MyDs*(2317)+ D- PHSP;',
'0.0015  D*- MyDs*(2317)+ SVS;',
'0.0027  MyDs*(2457)+ D- SVS;',
'0.0071  MyDs*(2457)+ D*- SVV_HELAMP 0.4904 0. 0.7204 0. 0.4904 0.;',

# these decays are not measured yet (not in PDG) and we take them from evtgen DEC

"0.0006     D'_1-   MyDs+               SVS;",
"0.001192   D'_1-   MyDs*+              SVV_HELAMP 0.48 0.0 0.734 0.0 0.48 0.0;",
"0.0012     D_1-    MyDs+               SVS;",
"0.002385   D_1-    MyDs*+              SVV_HELAMP 0.48 0.0 0.734 0.0 0.48 0.0;",
"0.0042     D_2*-   MyDs+               STS;",
"0.003975   D_2*-   MyDs*+              PHSP;",

"0.0018     MyDs+  D-  pi0             PHSP;",
"0.0037     MyDs+  anti-D0 pi-         PHSP;",
"0.001789   MyDs*+ D-  pi0             PHSP;",
"0.003677   MyDs*+ anti-D0 pi-         PHSP;",
"0.003      MyDs+  D-  pi-  pi+        PHSP;",
"0.0022     MyDs+  D-  pi0  pi0        PHSP;",
"0.0022     MyDs+  anti-D0 pi-  pi0    PHSP;",
"0.002981   MyDs*+ D-  pi-  pi+        PHSP;",
"0.002186   MyDs*+ D-  pi0  pi0        PHSP;",
"0.002186   MyDs*+ anti-D0 pi-  pi0    PHSP;",

'Enddecay ',
'CDecay Myanti-B0',

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
             '511:m0 = 5.27972',#pdg mass of B0 meson, pdg 2025
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
     MotherIDs       = cms.untracked.vint32 (431),   # Ds+
     ParticleID      = cms.untracked.int32  (333)    # Phi
)

DsToPhiPiFilter = cms.EDFilter(
     "PythiaFilterMultiAncestor",
     DaughterIDs     = cms.untracked.vint32 (  333,  -211), # phi, pion-
     DaughterMaxEtas = cms.untracked.vdouble( 2.55,  2.55),
     DaughterMaxPts  = cms.untracked.vdouble( 1.e9,  1.e9),
     DaughterMinEtas = cms.untracked.vdouble(-2.55, -2.55),
     DaughterMinPts  = cms.untracked.vdouble(  0.5,   0.5),
     MaxEta          = cms.untracked.double ( 99.0),
     MinEta          = cms.untracked.double (-99.0),
     MinPt           = cms.untracked.double (-1.0),
     MotherIDs       = cms.untracked.vint32 (5),
     ParticleID      = cms.untracked.int32  (-431) # Ds-
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


ProductionFilterSequence = cms.Sequence(generator + PhiToKKFromDsFilter + DsToPhiPiFilter + DsMuMaxMassFilter)












