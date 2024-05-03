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
      'MyB+',
      'MyB-',
      ),

      #remark PDG ID of Bs is (531), the default list is cms.vint32()
      operates_on_particles = cms.vint32(521,-521),
      convertPythiaCodes = cms.untracked.bool(False),

      user_decay_embedded = cms.vstring(

'Alias      MyB+         B+',
'Alias      MyB-         B-',
'ChargeConj MyB+         MyB-',
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

#Ds*(2317) decay, mode from LHCb:
#https://gitlab.cern.ch/lhcb-datapkg/Gen/DecFiles/-/blob/master/dkfiles/B+_DstXc,Xc2hhhNneutrals_cocktail_3pi,upto5prongs=DecProdC    ut.dec?ref_type=heads

'Decay MyDs*(2317)-',
'1.00000000 MyDs- pi0 PHSP; ',
'Enddecay',
'CDecay MyDs*(2317)+',

#Ds*(2457) decay, mode from LHCb:
#https://gitlab.cern.ch/lhcb-datapkg/Gen/DecFiles/-/blob/master/dkfiles/B+_DstXc,Xc2hhhNneutrals_cocktail_3pi,upto5prongs=DecProdC    ut.dec?ref_type=heads


# - MyDs*- gamma not present in the LHCb file, but it is in PDG, so we include it.
#   Its mode is motivated from MyDs*- gamma decay (Line 6687 in DECAY_NOLONGLFIE_2020.DEC)
# - LHCb is including the Ds pi0 pi0 final state, which we do not, as it is not in the PDG

'Decay MyDs*(2457)+',
'0.18           MyDs+          gamma           VSP_PWAVE;',
'0.48           MyDs*+         pi0             PHSP;',
'0.043          MyDs+          pi+     pi-     PHSP;',
'0.037          MyDs*(2317)+   gamma           VSP_PWAVE;',
'0.08           MyDs*+         gamma           PHSP;',
'Enddecay',
'CDecay MyDs*(2457)-',

# - Remark: GOITY_ROBERTS mode motivated from:
#   https://github.com/cms-data/GeneratorInterface-EvtGenInterface/blob/master/DECAY_2020_NOLONGLIFE.DEC#L5173C64-L5173C77, paper:     https://arxiv.org/abs/hep-ph/9406236
# - Tau nu_tau cases are calcualted from the muon BR with R = 0.2970, resp. R* = 0.2450

#BR and charges checked
'Decay MyB+',
'0.00030 MyDs- K+ mu+ nu_mu PHSP;',
'0.00009 MyDs- K+ tau+ nu_tau PHSP;',
'0.0090 MyDs+ anti-D0 PHSP; ',
'0.0082 anti-D*0 MyDs+ SVS; ',
'0.00029 MyDs*- K+ mu+ nu_mu PHSP;',
'0.00007 MyDs*- K+ tau+ nu_tau PHSP;',
'0.0008 MyDs*(2317)+ anti-D0 PHSP;',
'0.0009 anti-D*0 MyDs*(2317)+ SVS;',
'0.0031 MyDs*(2457)+ anti-D0 SVS;',
'0.0120 anti-D*0 MyDs*(2457)+ SVV_HELAMP 0.4904 0.0 0.7204 0.0 0.4904 0.0;',
'0.0076 MyDs*+ anti-D0 SVS; ',
'0.0171 MyDs*+ anti-D*0 SVV_HELAMP 0.48 0.0 0.734 0.0 0.48 0.0; ',
'Enddecay ',
'CDecay MyB-',
 
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
             '531:m0 = 5.36688',#mass of Bs meson
             '531:tau0 = 0.457783083', # in mm, consistent with EvtGen
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











