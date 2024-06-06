from __future__ import print_function
import ROOT
import argparse
import numpy as np
from time import time
from datetime import datetime, timedelta
from array import array
from glob import glob
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
parser.add_argument('--input'        , dest='input_file'   , required='True'  , type=str)
parser.add_argument('--output'       , dest='output_file'  , required='True'  , type=str)
parser.add_argument('--maxevents'    , dest='maxevents'    , default=-1       , type=int)
args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file
maxevents = args.maxevents

# Define branches
branch_names = [
    'run',
    'lumi',
    'event',

    
    'mu_pt',
    'mu_eta',
    'mu_y',
    'mu_phi',
    'mu_m',
    'mu_status',
    'b_pt',
    'b_eta',
    'b_y',
    'b_phi',
    'b_m',
    'b_dist',
    'b_tau',
    'b_status',
    'pi_pt',
    'pi_eta',
    'pi_y',
    'pi_phi',
    'pi_m',
    'pi_status',
    'kp_pt',
    'kp_eta',
    'kp_y',
    'kp_phi',
    'kp_m',
    'kp_status',
    'km_pt',
    'km_eta',
    'km_y',
    'km_phi',
    'km_m',
    'km_status',
    'ds_pt',
    'ds_eta',
    'ds_y',
    'ds_phi',
    'ds_m',
    'ds_status',
    'phi_m_from_kk',
    'ds_m_from_kkpi',
    'pv_x'  ,
    'pv_y'  ,
    'pv_z'  ,
    'sv_x'  ,
    'sv_y'  ,
    'sv_z'  ,
    'lxyz'  ,
    'kk_charge',
    'pimu_charge',
    'pids_charge',
    'ds_charge',
    'pi_charge',
    'kp_charge',
    'km_charge',
    'mu_charge',
    'b_charge',
    'cosbeta',
    'signal',
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

#we have 4 signal types: 
# Ds mu = 0
# Ds* mu = 1
# Ds tau = 2
# Ds* tau = 3
#start with 0 and change counter when we find a Ds* or tau
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


#miniAOD file(s) to process
if(os.path.isfile(input_file)):
    print("i am here!")
    #signle miniAOD file
    event_list = [Events(input_file)]
    path_mother = input_file.split("_fragment")[0]
    #mother = path_mother.split("pahwagne/")[1] old
    mother = path_mother.split("miniAOD/")[1]
    #mother = ["Bc+"]
if(os.path.isdir(input_file)):

    print("i am here2!")
    #folder of miniAOD files use TChain to stack
    event_list = []
    for tree in os.listdir(input_file):

        print("Investigating ", tree,)
        event_list.append(Events(input_file+ '/'+tree)) 
    mother = tree.split("_fragment")[0]


#prepare dict for handles
handles = OrderedDict()
handles['genParticle'   ] = ('genParticles', Handle('std::vector<reco::GenParticle>'))
handles['genInfo'] = ('generator'   , Handle('GenEventInfoProduct'           ))

#output flat root file
fout = ROOT.TFile(output_file, 'recreate')
ntuple = ROOT.TNtuple('tree', 'tree', ':'.join(branch_names))
branches = OrderedDict(zip(branch_names, [np.nan]*len(branch_names)))

#start time measurement
start = time()

global daughters 
daughters = []

print(event_list)
found = 0 
for events in event_list: 
  maxevents = maxevents if maxevents>=0 else events.size() 
  for i, event in enumerate(events):
      print("--------- NEW EVENT ----------" )  
  
      if (i+1)>maxevents: #maxevents
          break
          
      if i%100==0:
          
          percentage = float(i)/maxevents*100.
          speed = float(i)/(time()-start)
          #estimated time of arrival
          eta = datetime.now() + timedelta(seconds=(maxevents-i) / max(0.1, speed))
          
          print('\t===> processing %d / %d event \t completed %.1f%s \t %.1f ev/s \t ETA %s s' %(i, maxevents, percentage, '%', speed, eta.strftime('%Y-%m-%d %H:%M:%S')))
  # 
  
      # access the handles
      for key, tup in handles.items():
          
          event.getByLabel(tup[0], tup[1])
          
          #define new attributes for event
          #product returns the physical object
          setattr(event,key,tup[1].product())
  
      #make the qscale a direct attirbute of event
      event.qscale = event.genInfo.qScale()
  
      genP = event.genParticle
      genI = event.genInfo
      #pdb.set_trace() 
      #collect all Ds
      Ds  = [ip for ip in genP if abs(ip.pdgId())==431]
      #collect all Ds
      Dsstar  = [ip for ip in genP if abs(ip.pdgId())==433]
      #collect all final state muons (status = 1)
      Mu  = [ip for ip in genP if abs(ip.pdgId())==13 and ip.status()==1 and ip.pt()>0. and abs(ip.eta())<1.55]
      #collect all taus
      Tau = [ip for ip in genP if abs(ip.pdgId())==15]
      #colelct all Phis
      Phi = [ip for ip in genP if abs(ip.pdgId())==333]
      #collect mothers
      Bs  = [ip for ip in genP if abs(ip.pdgId())==motherids[mother]]
      print("B in event ", len(Bs)) 
      print("Ds in event ", len(Ds)) 

      #This for-loop was only used to test the forcing of evtgen
      #i.e. check the exact output and decays
  
      for bs in Bs:
          print("B meson with Id:", bs.pdgId())
          daus = [bs.daughter(i) for i in range(bs.numberOfDaughters())]        
          daus_id = [bs.daughter(i).pdgId() for i in range(bs.numberOfDaughters())]        
     
          print("This bs has daughters:", daus_id)
   
          for dau in daus:
              nd_daus = [dau.daughter(i).pdgId() for i in range(dau.numberOfDaughters())]
              nd_daus_p = [dau.daughter(i) for i in range(dau.numberOfDaughters())] 
              print("The particle ", dau.pdgId(), " has daughters: ", nd_daus)
  
              for dau in nd_daus_p:
                  rd_daus_id = [dau.daughter(i).pdgId() for i in range(dau.numberOfDaughters())]
                  rd_daus_p = [dau.daughter(i) for i in range(dau.numberOfDaughters())] 
                  print("The particle ", dau.pdgId(), " has daughters: ", rd_daus_id)
                  for dau in rd_daus_p:
                      fd_daus_id = [dau.daughter(i).pdgId() for i in range(dau.numberOfDaughters())]
                      #4d_daus_p = [dau.daughter(i) for i in range(dau.numberOfDaughters())] 
                      print("The particle ", dau.pdgId(), " has daughters: ", fd_daus_id)
          if len(daus_id) >1 : 
              daus_id.append([bs.pdgId()])
              daughters.append(daus_id)
          else:
              nd_daus.append(daus_id) 
              daughters.append(nd_daus)

      if len(Bs)==0:
          print([p.pdgId() for p in genP])
      """ 
      count1 = 0
      count2 = 0
      count3 = 0
      count4 = 0
      count5 = 0
      count6 = 0
      count7 = 0
      count8 = 0
      count9 = 0
      count10 = 0
      count11 = 0
      count12 = 0
      count1b = 0
      count2b = 0
      count3b = 0
      count4b = 0
      count5b = 0
      count6b = 0
      count7b = 0
      count8b = 0
      count9b = 0
      count10b = 0
      count11b = 0
      count12b = 0
      
      
      case1 = [-433,433,[531]]   
      case2 = [433,-433,[531]]   
      case1b = [-433,433,[-531]]   
      case2b = [433,-433,[-531]]   
      
      case3 = [-431,431,[531]]   
      case4 = [431,-431,[531]]   
      case3b = [-431,431,[-531]]   
      case4b = [431,-431,[-531]]   
      
      case5 = [433,-431,[531]]  
      case6 = [-433,431,[531]]  
      case7 = [431,-433,[531]]  
      case8 = [-431,433,[531]]  
      case5b = [433,-431,[-531]]  
      case6b = [-433,431,[-531]]  
      case7b = [431,-433,[-531]]  
      case8b = [-431,433,[-531]]  
      
      case9 = [-431,411,[531]]
      case10 = [431,-411,[531]]
      case11 = [-411,431,[531]]
      case12 = [411,-431,[531]]
      case9b = [-431,411,[-531]]
      case10b = [431,-411,[-531]]
      case11b = [-411,431,[-531]]
      case12b = [411,-431,[-531]]
      
      for dau in daughters:
      
          if dau == case1: count1 +=1
          if dau == case2: count2 +=1
          if dau == case3: count3 +=1
          if dau == case4: count4 +=1
          if dau == case5: count5 +=1
          if dau == case6: count6 +=1
          if dau == case7: count7 +=1
          if dau == case8: count8 +=1
          if dau == case9: count9 +=1
          if dau == case10: count10 +=1
          if dau == case11: count11 +=1
          if dau == case12: count12 +=1
          if dau == case1b: count1b +=1
          if dau == case2b: count2b +=1
          if dau == case3b: count3b +=1
          if dau == case4b: count4b +=1
          if dau == case5b: count5b +=1
          if dau == case6b: count6b +=1
          if dau == case7b: count7b +=1
          if dau == case8b: count8b +=1
          if dau == case9b: count9b +=1
          if dau == case10b: count10b +=1
          if dau == case11b: count11b +=1
          if dau == case12b: count12b +=1
      
      print("first column is Bs mother, second is anti Bs mother")
      print("Decay into -433,433:",count1, count1b, "should be equal")
      print("Decay into 433,-433:",count2, count2b, "should be equal")
      print("Decay into -431,431:",count3, count3b, "should be equal")
      print("Decay into 431,-431:",count4, count4b, "should be equal")
      print("Decay into 433,-431:",count5, count5b, "should be equal")
      print("Decay into -433,431:",count6, count6b, "should be equal")
      print("Decay into 431,-433:",count7, count7b, "should be equal")
      print("Decay into -431,433:",count8, count8b, "should be equal")
      print("Decay into -431,411:",count9, count9b, "should be equal")
      print("Decay into 431,-411:",count10, count10b, "should be equal")
      print("Decay into -411,431:",count11, count11b, "should be equal")
      print("Decay into 411,-431:",count12, count12b, "should be equal")
      """        
  
      #Loop over all Ds in decay
      for ds in Ds:
  
          signal = 0       
  
          #save pdgId of ds daughters
          ds_daus= [ds.daughter(idau).pdgId() for idau in range(ds.numberOfDaughters())]
        
          #only keep Ds -> PhiPi
          if ((ds_daus.count(333) < 1) or (ds_daus.count(211 * ds.charge()) < 1)): 
              continue
  
          #collect and print ancestors
          ancestors = []
          printAncestors(ds, ancestors) 
          if len(ancestors) == 0: continue
  
  
          #get the origin of the chain, the ultimate mom ;)
          chain_origin = ancestors[-1]
  
          if chain_origin in diquarks: 
  
              #we do not want a diquark mother
              chain_origin = ancestors[-2]
         
          print("The chain origin is: ", chain_origin.pdgId())
 
          if ((abs(chain_origin.pdgId())<500) or ((abs(chain_origin.pdgId())>600) and (abs(chain_origin.pdgId())<5000)) or (abs(chain_origin.pdgId())>6000)) : 
            print("This was a bad ds with no B mother")
            continue
  
          #if we made it this far, ds is a good ds:)
          print("This is a good ds")
          
          #now select good pi, and phi and mu
          pi_candidates = [ds.daughter(i) for i in range(ds.numberOfDaughters()) if ds.daughter(i).pdgId() == ds.charge()*211]
          phi_candidates = [ds.daughter(i) for i in range(ds.numberOfDaughters()) if ds.daughter(i).pdgId() == 333]
          tau_candidates = [tau for tau in Tau if isAncestor(chain_origin,tau)]

          #mu_candidates = [mu for mu in Mu if isAncestor(chain_origin,mu)] #only for signals!
          mu_candidates = Mu

          print(len(pi_candidates),len(mu_candidates), len(phi_candidates))   
 
          if (len(pi_candidates)) < 1  or (len(mu_candidates) < 1) or (len(phi_candidates) < 1): 
            print("However, no matching pi,mu or phi candidate found ->skip")
            continue
  
          #sort after momentum , highest first
          pi_candidates.sort(key=lambda x: x.pt(), reverse = True)
          mu_candidates.sort(key=lambda x: x.pt(), reverse = True)
          tau_candidates.sort(key=lambda x: x.pt(), reverse = True)
          phi_candidates.sort(key=lambda x: x.pt(), reverse = True)
  
          pi = pi_candidates[0]
          mu = mu_candidates[0]
          phi = phi_candidates[0]
  
          """ 
          #signals only
          if (len(tau_candidates) > 0):
              print("This is a tau candidate!")
              tau = tau_candidates[0]       
              mu_from_tau = [tau.daughter(i) for i in range(tau.numberOfDaughters()) if abs(tau.daughter(i).pdgId()) == 13 ] 
              mu_from_tau.sort(key=lambda x: x.pt(), reverse = True)
              mu = mu_from_tau[0]
              signal += 1
          """

          #get kp km for highest momentum phi (do not expect to have more than 1 phi.., but lets be sure)
          kp_candidates = [phi.daughter(i) for i in range(phi.numberOfDaughters()) if phi.daughter(i).pdgId() == 321]
          km_candidates = [phi.daughter(i) for i in range(phi.numberOfDaughters()) if phi.daughter(i).pdgId() == -321]
      
          if (len(km_candidates) < 1) or (len(kp_candidates)) < 1 : continue
  
          #get highest momentum kp, km 
          kp_candidates.sort(key=lambda x: x.pt(), reverse = True)
          km_candidates.sort(key=lambda x: x.pt(), reverse = True)
          kp = kp_candidates[0]
          km = km_candidates[0]
       
  
          found += 1        
   
          branches['run'        ] = event.eventAuxiliary().run()
          branches['lumi'       ] = event.eventAuxiliary().luminosityBlock()
          branches['event'      ] = event.eventAuxiliary().event()
          branches['b_pt'    ] = chain_origin.pt()
          branches['b_eta'   ] = chain_origin.eta()        
          branches['b_y'     ] = chain_origin.y()
          branches['b_phi'   ] = chain_origin.phi()
          branches['b_m'     ] = chain_origin.mass()
          branches['b_status'] = chain_origin.status()
          branches['ds_pt'    ] = ds.pt()
          branches['ds_eta'   ] = ds.eta()        
          branches['ds_y'     ] = ds.y()
          branches['ds_phi'   ] = ds.phi()
          branches['ds_m'     ] = ds.mass()
          branches['ds_status'] = ds.status()
          branches['pi_pt'    ] = pi.pt()
          branches['pi_eta'   ] = pi.eta()        
          branches['pi_y'     ] = pi.y()
          branches['pi_phi'   ] = pi.phi()
          branches['pi_m'     ] = pi.mass()
          branches['pi_status'] = pi.status()
          branches['mu_pt'    ] = mu.pt()
          branches['mu_eta'   ] = mu.eta()        
          branches['mu_y'     ] = mu.y()
          branches['mu_phi'   ] = mu.phi()
          branches['mu_m'     ] = mu.mass()
          branches['mu_status'] = mu.status()
          branches['kp_pt'    ] = kp.pt()
          branches['kp_eta'   ] = kp.eta()        
          branches['kp_y'     ] = kp.y()
          branches['kp_phi'   ] = kp.phi()
          branches['kp_m'     ] = kp.mass()
          branches['kp_status'] = kp.status()
          branches['km_pt'    ] = km.pt()
          branches['km_eta'   ] = km.eta()        
          branches['km_y'     ] = km.y()
          branches['km_phi'   ] = km.phi()
          branches['km_m'     ] = km.mass()
          branches['km_status'] = km.status()
          branches['kk_charge'] = km.charge()*kp.charge()   #should always be -1
          branches['pimu_charge'] = pi.charge()*mu.charge() #should always be -1
          branches['pids_charge'] = pi.charge()*ds.charge() #should always be 1
          branches['km_charge'] = km.charge()
          branches['kp_charge'] = kp.charge()
          branches['pi_charge'] = pi.charge()
          branches['mu_charge'] = mu.charge()
          branches['b_charge'] = chain_origin.charge()
          branches['signal'   ] = signal
  
  
          #the chain_origin (B hadron) defines the secondary vertex
          sv = chain_origin.vertex()
          #third vertex is given by ds
          tv = ds.vertex()
          # distance between sv and tv
          lxyz = np.sqrt((sv.x()-tv.x())**2 + (sv.y()-tv.y())**2 + (sv.z()-tv.z())**2)
  
          branches["sv_x"     ] = sv.x()
          branches["sv_y"     ] = sv.y()
          branches["sv_z"     ] = sv.z()
          branches["tv_x"     ] = tv.x()
          branches["tv_y"     ] = tv.y()
          branches["tv_z"     ] = tv.z()
          branches["lxyz"     ] = lxyz
          b_dist = np.sqrt(sv.x()**2 + sv.y()**2 + sv.z()**2)
          bvec = ROOT.Math.PtEtaPhiMVector(chain_origin.pt(),chain_origin.eta(),chain_origin.phi(),chain_origin.mass())

          branches['b_dist'  ] = b_dist
          b_tau = b_dist / (299792458 * bvec.Beta() * bvec.Gamma())
          branches['b_tau'  ] = b_tau
     
 
          kpvec = ROOT.Math.PtEtaPhiMVector(kp.pt(),kp.eta(),kp.phi(),kp.mass())
          kmvec = ROOT.Math.PtEtaPhiMVector(km.pt(),km.eta(),km.phi(),km.mass())
          pivec = ROOT.Math.PtEtaPhiMVector(pi.pt(),pi.eta(),pi.phi(),pi.mass())
          phivec = ROOT.Math.PtEtaPhiMVector(phi.pt(),phi.eta(),phi.phi(),phi.mass())

          kk = kpvec + kmvec
          kkpi = kk+ pivec
  
          branches['phi_m_from_kk'] = kk.M()
          branches['ds_m_from_kkpi'] = kkpi.M()
  
          #helicity angle calculation
          #it is the angle between on eof the K and the pi in the rest frame of the phi
  
          phi_beta = phivec.BoostToCM()        
  
          #does not work wheny you give phi_beta directly :)))))
          matrix = ROOT.Math.Boost((phi_beta.X(),phi_beta.Y(),phi_beta.Z()))
          kp_in_phi = matrix*kpvec
          pi_in_phi = matrix*pivec
  
          #and this also not works with .Dot(..) -.- 
          dummy = kp_in_phi.px()*pi_in_phi.px() + kp_in_phi.py()*pi_in_phi.py() + kp_in_phi.pz()* pi_in_phi.pz()
  
          cosbeta = dummy / (kp_in_phi.P()*pi_in_phi.P())
  
          branches["cosbeta"] = cosbeta
  
          try: 
            ntuple.Fill(array('f', branches.values()))
          except:
            continue
#daughters = [str(dau) for dau in daughters]
#daughters = list(dict.fromkeys(daughters))
#print(*daughters,sep='\n')

print("tree should contain :", found, " events") 

fout.cd()
ntuple.Write()
fout.Close()

