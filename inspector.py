from __future__ import print_function
import ROOT
import argparse
import numpy as np
from time import time
from datetime import datetime, timedelta
from array import array
import glob
from collections import OrderedDict
from scipy.constants import c as speed_of_light
from DataFormats.FWLite import Events, Handle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
# https://pypi.org/project/particle/
#from particle import Particle
import sys
import os.path
import pdb 
#Define command line inputs
parser = argparse.ArgumentParser(description='Inspect miniAOD and produce flat ntuples')
#parser.add_argument('--input'        , dest='input_file'   , required='True'  , type=str)
#parser.add_argument('--output'       , dest='output_file'  , required='True'  , type=str)
parser.add_argument('--maxevents'    , dest='maxevents'    , default=-1       , type=int)
args = parser.parse_args()

#input_file = args.input_file
#output_file = args.output_file
maxevents = args.maxevents

#input_file = '/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/mc/test/CEF9599E-F695-554B-97D2-276663715216.root'
#input_file = 'signals_test.root'
#input_file = 'root://storage01.lcg.cscs.ch:1096//pnfs/lcg.cscs.ch/cms/trivcat//store/user/pahwagne/2025Jun03/CRAB_PrivateMC/crab_20250603_151510/250603_131531/0000/hb_test_10.root'
#input_file ="root://storage01.lcg.cscs.ch:1096//pnfs/lcg.cscs.ch/cms/trivcat//store/user/pahwagne/2025Jun03/CRAB_PrivateMC/crab_20250603_181905/250603_161919/0000/hb_test_1.root"
#input_file = "root://cmsxrootd.fnal.gov///store/user/pahwagne/hbInclusiveToDsPhiKKPi/crab_20250605_133227/250605_113247/0000/hb_test_462.root"
input_file = "./signals_test.root"
#input_file = "/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/miniAOD/signals_fragment_17_07_2025_07_22_32/signals_fragment_chunk99_17_07_2025_07_22_32.root"

#input_file = "/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/miniAOD/hb_fragment_17_07_2025_07_22_44/hb_fragment_chunk1_17_07_2025_07_22_44.root" #old
#input_file = "/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/miniAOD/hb_fragment_12_08_2025_15_43_35/hb_fragment_chunk1_12_08_2025_15_43_35.root" #today

#input_file = "/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/miniAOD/signals_fragment_17_07_2025_07_22_32/signals_fragment_chunk5_17_07_2025_07_22_32.root" #old
input_files = "/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/miniAOD/signals_fragment_17_07_2025_07_22_32/" #old
#input_file = "/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/miniAOD/signals_fragment_12_08_2025_16_05_32/signals_fragment_chunk5_12_08_2025_16_05_32.root" #today
input_files = "/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/miniAOD/signals_fragment_12_08_2025_16_05_32/" #today


#test the seed
#input_files = "/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/miniAOD/signals_fragment_14_08_2025_09_07_33/" #with b quark filter
input_files = "/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/miniAOD/signals_fragment_14_08_2025_11_26_44/"#wout b quark filter



GENSIM = True 

import csv
def load_pdg_names(filepath):
    pdg_dict = {}
    with open(filepath, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pdg_dict[int(row["PDGID"])] = row["STR"]
    return pdg_dict

# Load it once
pdg_to_name = load_pdg_names("id_name_map.csv")

print(GENSIM)
# Define branches
branch_names = [
    'run',
#    'lumi',
    'event',
    
#    'mu_pt',
#    'mu_eta',
#    'mu_y',
#    'mu_phi',
#    'mu_m',
#    'mu_status',
#    'b_pt',
#    'b_eta',
#    'b_y',
#    'b_phi',
#    'b_m',
#    'b_dist',
#    'b_tau',
#    'b_status',
#    'pi_pt',
#    'pi_eta',
#    'pi_y',
#    'pi_phi',
#    'pi_m',
#    'pi_status',
#    'kp_pt',
#    'kp_eta',
#    'kp_y',
#    'kp_phi',
#    'kp_m',
#    'kp_status',
#    'km_pt',
#    'km_eta',
#    'km_y',
#    'km_phi',
#    'km_m',
#    'km_status',
#    'ds_pt',
#    'ds_eta',
#    'ds_y',
#    'ds_phi',
#    'ds_m',
#    'ds_status',
#    'phi_m_from_kk',
#    'ds_m_from_kkpi',
#    'pv_x'  ,
#    'pv_y'  ,
#    'pv_z'  ,
#    'sv_x'  ,
#    'sv_y'  ,
#    'sv_z'  ,
#    'lxyz'  ,
#    'kk_charge',
#    'pimu_charge',
#    'pids_charge',
#    'ds_charge',
#    'pi_charge',
#    'kp_charge',
#    'km_charge',
#    'mu_charge',
#    'b_charge',
#    'cosbeta',
#    'signal',
]

#pdg number of diquarks

diquarks = [
    1103,
    2101,
    2103,
    2203,
    3101,
    3103,
    3201,
    3203,
    3303,
    4101,
    4103,
    4201,
    4203,
    4301,
    4303,
    4403,
    5101,
    5103,
    5201,
    5203,
    5301,
    5303,
    5401,
    5403,
    5503,
]

#motherids = {"Bs": 531, "B0":511, "B+":521 ,"Bc+":541 , "LambdaB":5122, "signals": 531} #old
motherids = {"bs": 531, "b0":511, "bplus":521 ,"bc":541 , "lambdab":5122, "signals": 531}

signal = 0


def printAncestors(genParticle, ancestors):

    global signal

    #loop over all mothers of genParticle
    for i in range(genParticle.numberOfMothers()):
        #get the mother 
        try:
            mot = genParticle.mother(i)
            if (abs(mot.pdgId()) == 433): 
                print("Found Ds*") 
                signal += 2               
            
            #if mother is a quark or gluon
            if abs(mot.pdgId())<8 or abs(mot.pdgId())==21: continue
            #???
            #if not mum.isLastCopy(): continue
 
            print("Mother of particle with ID ", genParticle.pdgId() ," is ----> ", mot.pdgId())
            ancestors.append(mot)

            #call again!
            printAncestors(mot,ancestors)

        except:
            print("End of chain, found no ancestor")
    print("done")


def printDaughters(mom):

    daus    = [mom.daughter(i).pdgId() for i in range(mom.numberOfDaughters())]        
    print("This mom with Id: ", mom.pdgId(), " has daughters: ", daus)

    for i in range(mom.numberOfDaughters()):
      printDaughters(mom.daughter(i))       

def printMothers(dau):

    moms = [dau.mother(i).pdgId() for i in range(dau.numberOfMothers())]        
    print("This dau with Id: ", dau.pdgId(), " has moms: ", moms)

    for i in range(dau.numberOfMothers()):
      printMothers(dau.mother(i))       

def getDaughter(mom, dau_id):

    for i in range(mom.numberOfDaughters()):
      if abs(mom.daughter(i).pdgId()) == dau_id:
        return mom.daughter(i)
    print("WARNING: No dau with id: ", dau_id, " found")
    return None

def isAncestorViaID(motId,dau):

    moms = [dau.mother(i).pdgId() for i in range(dau.numberOfMothers())]
    #print("At dau with Id: ", dau.pdgId(), "which has moms: ", moms)

    #if abs(motId) == abs(dau.pdgId()):
    #  return True

    ##if not there call function again
    #for i in range(0,dau.numberOfMothers()):
    #  #print("call again with mother: ", dau.mother(i).pdgId())
    #  if isAncestorViaID(motId, dau.mother(i)):
    #    return True

    ##if no mother found, return False
    #return False

   
    #test this 
    for m in moms:
      if abs(motId) == abs(m): return True
    else: return False 
 

def isAncestor(mot,dau):
    # checks if mot is a mother (of any generation) of dau
  
    #already there
    if mot == dau:
        return True

    #if not there call function again
    for i in range(0,dau.numberOfMothers()):
        if isAncestor(mot, dau.mother(i)):
            return True
    #if no mother found, return False
    return False

def isDaughter(mot,dau):
    # checks if dau is a daughter (of any generation) of mom
    #print("current mom is", mot.pdgId(), "and dau is ", dau.pdgId(), "daughters") 
 
    #already there
    if mot == dau:
        return True

    if mot.numberOfDaughters() == 0:
      #print("Exiting here, no daus")
      return False

    #if not there call function again
    for i in range(0,mot.numberOfDaughters()):
        #print("call again!")
        if isDaughter(mot.daughter(i), dau):
            return True
    #if no daughter found, return False
    return False


def isAncestorRicc(particle, IDtoMatch):
    vtx = particle.production_vertex()
    if not vtx:
        return False

    ancestor_it = vtx.particles_begin(ROOT.HepMC.ancestors)
    ancestor_end = vtx.particles_end(ROOT.HepMC.ancestors)

    while ancestor_it != ancestor_end:
        ancestor = ancestor_it.__deref__()
        if abs(ancestor.pdg_id()) == abs(IDtoMatch):
            return True
        ancestor_it.__preinc__()

    return False


#miniAOD file(s) to process
#if(os.path.isfile(input_file)):

if True:
  if GENSIM == True:
    #signle miniAOD file
    files = glob.glob(input_files + "*")[:10]
    event_list = [Events(f) for f in files]
    #event_list = [Events(input_file)]
    #path_mother = input_file.split("_fragment")[0]
    #mother = path_mother.split("miniAOD/")[1]
    mother = "bs"
  else:
    #signle miniAOD file
    event_list = [Events(input_file)]
    #path_mother = input_file.split("25mar21_v1/inclusive_")[1]
    #mother = path_mother.split("pahwagne/")[1] old
    #mother = path_mother.split("ToDsPhi")[0]
    mother = "bs"
  
import pdb

#prepare dict for handles

handles = OrderedDict()
if GENSIM == True:
  handles['genParticle'   ] = ('genParticles',     Handle('std::vector<reco::GenParticle>'))
  handles['hepMC'         ] = ('generatorSmeared', Handle('edm::HepMCProduct'))
  handles['genInfo'       ] = ('generator'       , Handle('GenEventInfoProduct'))

else:
  handles['genParticle'   ] = ('prunedGenParticles', Handle('std::vector<reco::GenParticle>'))
  handles['genInfo'] = ('generator'   , Handle('GenEventInfoProduct'           ))

#output flat root file
#fout     = ROOT.TFile(output_file, 'recreate')
ntuple   = ROOT.TNtuple('tree', 'tree', ':'.join(branch_names))
branches = OrderedDict(zip(branch_names, [np.nan]*len(branch_names)))

#start time measurement
start = time()

global daughters 
daughters = []

print(event_list)
found = 0 

evt_counter = 0
bad_events  = 0
noBMom      = 0
totevents   = 0

final_B = []
final_B_decay = []
for events in event_list: 

  ##################################
  # Start loop over miniAOD evens  #
  ##################################

  maxevents = maxevents if maxevents>=0 else events.size() 
  totevents += maxevents

  for i, event in enumerate(events):

      print("--------- NEW EVENT ----------" )  
      print("event id: ", event.eventAuxiliary().id().event())  
      if event.eventAuxiliary().id().event() != 4499: continue;

      if (i+1)>maxevents: #maxevents
          break
          
      if i%100==0:
          
          percentage = float(i)/maxevents*100.
          speed = float(i)/(time()-start)
          eta = datetime.now() + timedelta(seconds=(maxevents-i) / max(0.1, speed))
          
          print('\t===> processing %d / %d event \t completed %.1f%s \t %.1f ev/s \t ETA %s s' %(i, maxevents, percentage, '%', speed, eta.strftime('%Y-%m-%d %H:%M:%S')))
  # 
  
      # access the handles
      for key, tup in handles.items():
          
          event.getByLabel(tup[0], tup[1])
          #product returns the physical object
          setattr(event,key,tup[1].product())
  
     
      genP = event.genParticle
      genH = event.hepMC
      genI = event.genInfo


      # first, loop over hepMC particles
      evt = genH.GetEvent()
      it  = evt.particles_begin()
      end = evt.particles_end()
  
      hep_bs = []
      while it != end:
          p = it.__deref__()  # get HepMC::GenParticle
          p_id = p.pdg_id()
          if abs(p_id) == 431: hep_bs.append(p)
          it.__preinc__()     


      print("I found: ", len(hep_bs), " hep particles")

      for bs in hep_bs:

        if isAncestorRicc(bs,5): print("found b quark anc")
        else: print("no b quark anc")

        #print(" for this mom the ancestors are: ")
        #vtx = bs.production_vertex()
        #if not vtx: continue
        #ancestor_it = vtx.particles_begin(ROOT.HepMC.ancestors)
        #ancestor_end = vtx.particles_end(ROOT.HepMC.ancestors)

        #while ancestor_it != ancestor_end:
        #  anc = ancestor_it.__deref__()  
        #  print("ancestor with id: ", anc.pdg_id())
        #  ancestor_it.__preinc__()

        good_dau = 0
        good_dau_cc = 0
       
        daughterIDs     = [333] 

        daughterMinPts  = [0.0]
        daughterMaxPts  = [1e9]

        daughterMinEtas = [-1e9]
        daughterMaxEtas = [1e9]

        end_vtx = bs.end_vertex()
        if end_vtx:  # safety check
            dau_it = end_vtx.particles_begin(ROOT.HepMC.children)
            dau_end = end_vtx.particles_end(ROOT.HepMC.children)
        
            while dau_it != dau_end:
                dau = dau_it.__deref__()
        
                for i in range(len(daughterIDs)):
                    dau_id = dau.pdg_id()
                    pt = dau.momentum().perp()
                    eta = dau.momentum().eta()
        
                    # Normal PDG ID match
                    if dau_id == daughterIDs[i]:
                        if pt < daughterMinPts[i]:
                            dau_it.__preinc__()
                            continue
                        if pt > daughterMaxPts[i]:
                            dau_it.__preinc__()
                            continue
                        if eta < daughterMinEtas[i]:
                            dau_it.__preinc__()
                            continue
                        if eta > daughterMaxEtas[i]:
                            dau_it.__preinc__()
                            continue
                        good_dau += 1
        
                    # Charge conjugation PDG ID match
                    if -dau_id == daughterIDs[i]:
                        if pt < daughterMinPts[i]:
                            dau_it.__preinc__()
                            continue
                        if pt > daughterMaxPts[i]:
                            dau_it.__preinc__()
                            continue
                        if eta < daughterMinEtas[i]:
                            dau_it.__preinc__()
                            continue
                        if eta > daughterMaxEtas[i]:
                            dau_it.__preinc__()
                            continue
                        good_dau_cc += 1
        
                dau_it.__preinc__()
        
        if good_dau < len(daughterIDs) and good_dau_cc < len(daughterIDs):
            accepted = False
            print("i throw this event away")
          
        else:
            print("i keep this event!") 


      #collect all Ds
      Ds  = [ip for ip in genP if abs(ip.pdgId())==431]
      #collect all Ds*
      Dsstar  = [ip for ip in genP if abs(ip.pdgId())==433]
      #collect all final state muons (status = 1)
      Mu  = [ip for ip in genP if abs(ip.pdgId())==13 and ip.status()==1 and ip.pt()>0. and abs(ip.eta())<1.55]
      #collect all taus
      Tau = [ip for ip in genP if abs(ip.pdgId())==15]
      #colelct all Phis
      Phi = [ip for ip in genP if abs(ip.pdgId())==333]
      #collect B mothers
      Bs  = [ip for ip in genP if abs(ip.pdgId()) in np.concatenate((np.arange(500, 600), np.arange(5000, 6000)))  ] #allow all B moms
      #collect kaons
      ks  = [ip for ip in genP if abs(ip.pdgId())==321]

      #print("Ds are:", [d.pdgId() for d in Ds])
      if (len(Ds) == 0 or len(Mu) == 0): 
        #print("This event has no Ds or no Muons!")
        continue

      # check that the B-moms are not coming from the same chain! 
      # F.e. a decay like 531 -> 511 + X -> ... would list two Bs, but there is only one "decay chain"
      #print("before cleaning: ", [bs.pdgId() for bs in Bs])
      Bs_cleaned = []

      #loop over all b candidates ...
      for mom in Bs:
         
        #and check if any other b candidate is its daughter!
        has_b_dau = False

        print("pt of this bs is: ", mom.pt())

        for dau in Bs:
          if dau != mom: 
            if isDaughter(mom,dau): has_b_dau = True
       
        #if no B dau was found, the particle is the last of its kind and thus appended to the Bs 
        if not has_b_dau: Bs_cleaned.append(mom)

      #rename
      Bs = Bs_cleaned
      #This for-loop was only used to test the forcing of evtgen
      #i.e. check the exact output and decays
 
 
      #print("------ Check all B ancestors -------")

      #foundOne = 0
      for bs in Bs:
          # printDaughters(bs)
          #printMothers(bs)
          #print("Check bs: ", bs.pdgId())
          if not isAncestorViaID(5,bs): 
            noBMom += 1
          #else: foundOne += 1

      #if foundOne == 0: continue


      ##################################################
      # From all b-mom, select only signal like decays #
      ##################################################

      good_Bs = []
      # keep only Bs, which have a Ds(->KKPi) and mu as child
      for b in Bs:

        #print("-- check new b cand -- ", b.pdgId())
        has_good_ds_dau = False
        has_good_mu_dau = False

        for d in Ds:
          #print("-- check new ds cand -- ", d.pdgId())

          #keep only daughters
          if not isDaughter(b,d)       : #print(d.pdgId(), " no daughter of", b.pdgId()); 
            continue;

          #we only want ds -> phi pi
          d_daus = [abs(d.daughter(i).pdgId()) for i in range(d.numberOfDaughters())]
          #if len(d_daus) != 2          : print(d.pdgId(), " does not decay into phipi"); continue; 

          d_daus = set(d_daus)
          if (d_daus != {333,211} and d_daus != {333,211,22})     : 
            #print(d.pdgId(), " does not decay into phipi"); 
            continue; 

          #get pi
          pi = getDaughter(d,211) 
          #pi must have same charge as ds
          if pi.charge() != d.charge() : #print(" pi daughter has wrong charge");         
            continue;

          #get phi
          phi = getDaughter(d,333)

          #we only want phi -> K K
          phi_daus = [abs(phi.daughter(i).pdgId()) for i in range(phi.numberOfDaughters())]
          if len(phi_daus) != 2        : #print(phi.pdgId(), " does not decay into KK");  
            continue;

          phi_daus = set(phi_daus)
          if phi_daus != {321}         : #print(phi.pdgId(), " does not decay into KK");  
            continue; 

          #last but not least, check that KK are opposite charge (must be!)
          if phi.daughter(0).charge() == phi.daughter(1).charge(): #print("KK are not opposite charge"); 
            continue;

          #if we survived until here, this is a good ds
          has_good_ds_dau = True 
  
       
        for m in Mu:

          #keep only daughters
          if not isDaughter(b,m)        : #print(m.pdgId(), "is not daughter of", b.pdgId()); 
            continue;
   
          has_good_mu_dau = True 
        
        if has_good_ds_dau and has_good_mu_dau: 
          #this is a good b mom!
          good_Bs.append(b)

      if len(good_Bs) == 0: 
        bad_events += 1
        continue;
      else: 
        evt_counter += 1

      for bs in good_Bs:
          print("------ NEW good B IN THE EVENT -------")
          printDaughters(bs)


      #now save the decay info!

      #save the moms and their daughters
      for b in good_Bs:
        final_B.append(pdg_to_name[abs(b.pdgId())])

        b_daus = [pdg_to_name[abs(b.daughter(i).pdgId())] for i in range(b.numberOfDaughters())]
        final_B_decay.append(b_daus)

      with open("B_moms.csv", 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for b in final_B:
          wr.writerow([b]) 

      with open("B_mom_decays.csv", 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for decay in final_B_decay:
          wr.writerow([decay]) 

      

 
      ##Loop over all Ds in decay
      #print("---- After the b loop, loop over d ----")
      #for ds in Ds:
  
      #    signal = 0       
  
      #    #save pdgId of ds daughters
      #    ds_daus= [ds.daughter(idau).pdgId() for idau in range(ds.numberOfDaughters())]
      #    print("This Ds has daughters: ", ds_daus)
      #  
      #    #only keep Ds -> PhiPi
      #    if ((ds_daus.count(333) < 1) or (ds_daus.count(211 * ds.charge()) < 1)): 
      #        continue
  
      #    #collect and print ancestors
      #    ancestors = []
      #    printAncestors(ds, ancestors) 
      #    if len(ancestors) == 0: continue
  
  
      #    #get the origin of the chain, the ultimate mom ;)
      #    chain_origin = ancestors[-1]
  
      #    if chain_origin in diquarks: 
  
      #        #we do not want a diquark mother
      #        chain_origin = ancestors[-2]
      #   
      #    print("The chain origin is: ", chain_origin.pdgId())
 
      #    #if ((abs(chain_origin.pdgId())<500) or ((abs(chain_origin.pdgId())>600) and (abs(chain_origin.pdgId())<5000)) or (abs(chain_origin.pdgId())>6000)) : 
      #    #  print("This was a bad ds with no B mother")
      #    #  continue
  
      #    b_ancestors = [ anc for anc in ancestors if ( ( abs(anc.pdgId())>=500 and abs(anc.pdgId())<600) or (abs(anc.pdgId())>=5000 and abs(anc.pdgId())< 6000 ) ) ] 
      #    if len(b_ancestors) < 1 : 
      #      print ("ds not coming from b mom :(")
      #      continue

      #    #if we made it this far, ds is a good ds:)
      #    print("This is a good ds")
      #    
      #    #now select good pi, and phi and mu
      #    pi_candidates = [ds.daughter(i) for i in range(ds.numberOfDaughters()) if ds.daughter(i).pdgId() == ds.charge()*211]
      #    phi_candidates = [ds.daughter(i) for i in range(ds.numberOfDaughters()) if ds.daughter(i).pdgId() == 333]
      #    tau_candidates = [tau for tau in Tau if isAncestor(chain_origin,tau)]

      #    #mu_candidates = [mu for mu in Mu if isAncestor(chain_origin,mu)] #only for signals!
      #    mu_candidates = Mu

      #    print(len(pi_candidates),len(mu_candidates), len(phi_candidates))   
 
      #    if (len(pi_candidates)) < 1  or (len(mu_candidates) < 1) or (len(phi_candidates) < 1): 
      #      print("However, no matching pi,mu or phi candidate found ->skip")
      #      continue
  
      #    #sort after momentum , highest first
      #    pi_candidates.sort(key=lambda x: x.pt(), reverse = True)
      #    mu_candidates.sort(key=lambda x: x.pt(), reverse = True)
      #    tau_candidates.sort(key=lambda x: x.pt(), reverse = True)
      #    phi_candidates.sort(key=lambda x: x.pt(), reverse = True)
  
      #    pi = pi_candidates[0]
      #    mu = mu_candidates[0]
      #    phi = phi_candidates[0]
  
      #    """ 
      #    #signals only
      #    if (len(tau_candidates) > 0):
      #        print("This is a tau candidate!")
      #        tau = tau_candidates[0]       
      #        mu_from_tau = [tau.daughter(i) for i in range(tau.numberOfDaughters()) if abs(tau.daughter(i).pdgId()) == 13 ] 
      #        mu_from_tau.sort(key=lambda x: x.pt(), reverse = True)
      #        mu = mu_from_tau[0]
      #        signal += 1
      #    """

      #    #get kp km for highest momentum phi (do not expect to have more than 1 phi.., but lets be sure)
      #    kp_candidates = [phi.daughter(i) for i in range(phi.numberOfDaughters()) if phi.daughter(i).pdgId() == 321]
      #    km_candidates = [phi.daughter(i) for i in range(phi.numberOfDaughters()) if phi.daughter(i).pdgId() == -321]
      #
      #    if (len(km_candidates) < 1) or (len(kp_candidates)) < 1 : continue
  
      #    #get highest momentum kp, km 
      #    kp_candidates.sort(key=lambda x: x.pt(), reverse = True)
      #    km_candidates.sort(key=lambda x: x.pt(), reverse = True)
      #    kp = kp_candidates[0]
      #    km = km_candidates[0]
      # 
  
      #    found += 1        
   
      #    branches['run'        ] = event.eventAuxiliary().run()
      #    branches['lumi'       ] = event.eventAuxiliary().luminosityBlock()
      #    branches['event'      ] = event.eventAuxiliary().event()
      #    branches['b_pt'    ] = chain_origin.pt()
      #    branches['b_eta'   ] = chain_origin.eta()        
      #    branches['b_y'     ] = chain_origin.y()
      #    branches['b_phi'   ] = chain_origin.phi()
      #    branches['b_m'     ] = chain_origin.mass()
      #    branches['b_status'] = chain_origin.status()
      #    branches['ds_pt'    ] = ds.pt()
      #    branches['ds_eta'   ] = ds.eta()        
      #    branches['ds_y'     ] = ds.y()
      #    branches['ds_phi'   ] = ds.phi()
      #    branches['ds_m'     ] = ds.mass()
      #    branches['ds_status'] = ds.status()
      #    branches['pi_pt'    ] = pi.pt()
      #    branches['pi_eta'   ] = pi.eta()        
      #    branches['pi_y'     ] = pi.y()
      #    branches['pi_phi'   ] = pi.phi()
      #    branches['pi_m'     ] = pi.mass()
      #    branches['pi_status'] = pi.status()
      #    branches['mu_pt'    ] = mu.pt()
      #    branches['mu_eta'   ] = mu.eta()        
      #    branches['mu_y'     ] = mu.y()
      #    branches['mu_phi'   ] = mu.phi()
      #    branches['mu_m'     ] = mu.mass()
      #    branches['mu_status'] = mu.status()
      #    branches['kp_pt'    ] = kp.pt()
      #    branches['kp_eta'   ] = kp.eta()        
      #    branches['kp_y'     ] = kp.y()
      #    branches['kp_phi'   ] = kp.phi()
      #    branches['kp_m'     ] = kp.mass()
      #    branches['kp_status'] = kp.status()
      #    branches['km_pt'    ] = km.pt()
      #    branches['km_eta'   ] = km.eta()        
      #    branches['km_y'     ] = km.y()
      #    branches['km_phi'   ] = km.phi()
      #    branches['km_m'     ] = km.mass()
      #    branches['km_status'] = km.status()
      #    branches['kk_charge'] = km.charge()*kp.charge()   #should always be -1
      #    branches['pimu_charge'] = pi.charge()*mu.charge() #should always be -1
      #    branches['pids_charge'] = pi.charge()*ds.charge() #should always be 1
      #    branches['km_charge'] = km.charge()
      #    branches['kp_charge'] = kp.charge()
      #    branches['pi_charge'] = pi.charge()
      #    branches['mu_charge'] = mu.charge()
      #    branches['b_charge'] = chain_origin.charge()
      #    branches['signal'   ] = signal
  
  
      #    #the chain_origin (B hadron) defines the secondary vertex
      #    sv = chain_origin.vertex()
      #    #third vertex is given by ds
      #    tv = ds.vertex()
      #    # distance between sv and tv
      #    lxyz = np.sqrt((sv.x()-tv.x())**2 + (sv.y()-tv.y())**2 + (sv.z()-tv.z())**2)
  
      #    branches["sv_x"     ] = sv.x()
      #    branches["sv_y"     ] = sv.y()
      #    branches["sv_z"     ] = sv.z()
      #    branches["tv_x"     ] = tv.x()
      #    branches["tv_y"     ] = tv.y()
      #    branches["tv_z"     ] = tv.z()
      #    branches["lxyz"     ] = lxyz
      #    b_dist = np.sqrt(sv.x()**2 + sv.y()**2 + sv.z()**2)
      #    bvec = ROOT.Math.PtEtaPhiMVector(chain_origin.pt(),chain_origin.eta(),chain_origin.phi(),chain_origin.mass())

      #    branches['b_dist'  ] = b_dist
      #    b_tau = b_dist / (299792458 * bvec.Beta() * bvec.Gamma())
      #    branches['b_tau'  ] = b_tau
     
 
      #    kpvec = ROOT.Math.PtEtaPhiMVector(kp.pt(),kp.eta(),kp.phi(),kp.mass())
      #    kmvec = ROOT.Math.PtEtaPhiMVector(km.pt(),km.eta(),km.phi(),km.mass())
      #    pivec = ROOT.Math.PtEtaPhiMVector(pi.pt(),pi.eta(),pi.phi(),pi.mass())
      #    phivec = ROOT.Math.PtEtaPhiMVector(phi.pt(),phi.eta(),phi.phi(),phi.mass())

      #    kk = kpvec + kmvec
      #    kkpi = kk+ pivec
  
      #    branches['phi_m_from_kk'] = kk.M()
      #    branches['ds_m_from_kkpi'] = kkpi.M()
  
      #    #helicity angle calculation
      #    #it is the angle between on eof the K and the pi in the rest frame of the phi
  
      #    phi_beta = phivec.BoostToCM()        
  
      #    #does not work wheny you give phi_beta directly :)))))
      #    matrix = ROOT.Math.Boost((phi_beta.X(),phi_beta.Y(),phi_beta.Z()))
      #    kp_in_phi = matrix*kpvec
      #    pi_in_phi = matrix*pivec
  
      #    #and this also not works with .Dot(..) -.- 
      #    dummy = kp_in_phi.px()*pi_in_phi.px() + kp_in_phi.py()*pi_in_phi.py() + kp_in_phi.pz()* pi_in_phi.pz()
  
      #    cosbeta = dummy / (kp_in_phi.P()*pi_in_phi.P())
  
      #    branches["cosbeta"] = cosbeta
  
      #    try: 
      #      ntuple.Fill(array('f', branches.values()))
      #    except:
      #      continue

  #print("In this file we found: ", evt_counter, " events")
  #print("In this file we found: ", bad_events , " bad events")
  #print("In this file we found: ", noBMom     , " events with no b quark mom")
  #print("And we had: ", maxevents, " to begin with")

print("we found: ", evt_counter, " events")
print("we found: ", bad_events , " bad events")
print("we found: ", noBMom     , " b hadrons with no b quark mom")
print("And we had: ", totevents , " to begin with")


#daughters = [str(dau) for dau in daughters]
#daughters = list(dict.fromkeys(daughters))
#print(*daughters,sep='\n')

#print("tree should contain :", found, " events") 
#
#fout.cd()
#ntuple.Write()
#fout.Close()
#



