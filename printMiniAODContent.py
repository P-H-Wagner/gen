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
import pdb 
import csv
import os

#Define command line inputs
parser = argparse.ArgumentParser(description='Inspect miniAOD and produce flat ntuples')
parser.add_argument('--inputFiles'   , nargs='+'        , required='True'  )
parser.add_argument('--outputFolder' , required='True'  , type=str)
parser.add_argument('--maxevents'    , default=-1       , type=int)
parser.add_argument('--maxfiles'     , default=-1       , type=int)
parser.add_argument('--GENSIM'       , default=True     , type=bool)
parser.add_argument('--debug'        , default=False    , type=bool)
parser.add_argument('--chunk'        , default=0        , type=int)
args = parser.parse_args()


inputFiles   = args.inputFiles
outputFolder = args.outputFolder
maxevents    = args.maxevents
maxfiles     = args.maxfiles
GENSIM       = args.GENSIM
debug        = args.debug
chunk        = args.chunk

# painful python 2
fout = "./" + outputFolder + "/"
os.system("mkdir -p " + fout)
os.system("mkdir -p " + fout + "/B_moms/")
os.system("mkdir -p " + fout + "/B_mom_decays/")
#inputFiles = "root://cmsxrootd.fnal.gov///store/user/pahwagne/hbInclusiveToDsPhiKKPi/crab_20250605_133227/250605_113247/0000/hb_test_462.root"

#path ="/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/mc/hb/inclusive/private_prod/hb_inclusive_crab_20250605_133227.txt"
#with open(path) as f:
#    inputFiles = f.read().splitlines()
#inputFiles = inputFiles[0:5000]

###############################
# Convert pdg id to name      #
###############################

def load_pdg_names(filepath):
    pdg_dict = {}
    with open(filepath, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pdg_dict[int(row["PDGID"])] = row["STR"]
    return pdg_dict

# mapping 
pdg_to_name = load_pdg_names("id_name_map.csv")

################################
# useful (recursive) functions #
################################

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

def getDaughter(mom, dau_id):

    for i in range(mom.numberOfDaughters()):
      if abs(mom.daughter(i).pdgId()) == dau_id:
        return mom.daughter(i)
    print("WARNING: No dau with id: ", dau_id, " found")
    return None

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
    #print("current mom is", mot.pdgId(), "and  has ", mot.numberOfDaughters(), "daughters") 
 
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


def filesFromFolder(direc):
  filenames = os.listdir(direc)
  return [direc + filename for filename in filenames ]

def filesFromTxt(txtFile):
  with open(txtFile) as dataFiles:
    filenames = [line[0:-1] for line in dataFiles] #-2 to remove the newline character \n
  return ['root://cms-xrd-global.cern.ch//' + filename for filename in filenames ]


#############################
# Prepare input             #
#############################

print(" =====> prepare input")

#inputFiles = [ "root://cmsxrootd.fnal.gov///" + f for f in inputFiles]
inputFiles = [ "root://cms-xrd-global.cern.ch///" + f for f in inputFiles]
#inputFiles = [ "root://xrootd-cms.infn.it//" + f for f in inputFiles]
#inputFiles = [ "root://xrootd-cms.infn.it//" + f for f in inputFiles]

#input files can be either given as .txt file or as directory
#if ".txt" in inputFiles:
#  inputFiles = filesFromTxt(inputFiles)
#
#elif ".root" in inputFiles:
#  inputFiles = [inputFiles]
#
#else:
#  inputFiles = filesFromFolder(inputFiles)
#
#if maxfiles != -1:
#  inputFiles = inputFiles[:maxfiles]

#now inputFiles is a list

print(" =====> get events")
#event_list = [Events(f) for f in inputFiles]

#############################
# Prepare handles           #
#############################

#handles = OrderedDict()

#if GENSIM :
#  handles['genParticle'   ] = ('genParticles', Handle('std::vector<reco::GenParticle>'))
#  handles['genInfo']        = ('generator'   , Handle('GenEventInfoProduct'           ))
#
#else:
#  handles['genParticle'   ] = ('prunedGenParticles', Handle('std::vector<reco::GenParticle>'))
#  handles['genInfo']        = ('generator'   , Handle('GenEventInfoProduct'           ))

#start time measurement
start = time()

def processFile(f,maxevents,debug):

  events = Events(f)

  #empty list which will hold the decays we write to the csv files
  
  good_Bs_str        = []
  good_Bs_decays_str = []

  handles = OrderedDict()
  handles['genParticle'   ] = ('genParticles', Handle('std::vector<reco::GenParticle>'))
  handles['genInfo']        = ('generator'   , Handle('GenEventInfoProduct'           ))

  maxevents = maxevents if maxevents>=0 else events.size() 

  # ... and loop over them         
  for i, event in enumerate(events):

      if debug:
        print("--------- NEW EVENT ----------" )  
        print("event id: ", event.eventAuxiliary().id().event())  
        #if event.eventAuxiliary().id().event() != 46193148: continue;

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
      genI = event.genInfo

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


      # check that the B-moms are not coming from the same chain! 
      # F.e. a decay like 531 -> 511 + X -> ... would list two Bs, but there is only one "decay chain"

      Bs_cleaned = []

      #loop over all b candidates ...
      for mom in Bs:
         
        #and check if any other b candidate is its daughter!
        has_b_dau = False

        for dau in Bs:
          if dau != mom: 
            if isDaughter(mom,dau): has_b_dau = True
       
        #if no B dau was found, the particle is the last of its kind and thus appended to the Bs 
        if not has_b_dau: Bs_cleaned.append(mom)

      #rename
      Bs = Bs_cleaned

      if debug: 
        for bs in Bs:
            print("------ NEW B IN THE EVENT -------")
            printDaughters(bs)

      ##################################################
      # From all b-mom, select only signal like decays #
      ##################################################

      good_Bs = []
      # keep only Bs, which have a Ds(->KKPi) and mu as child

      for b in Bs:

        has_good_ds_dau = False
        has_good_mu_dau = False

        for d in Ds:

          #keep only daughters
          if not isDaughter(b,d)       : continue;

          #we only want ds -> phi pi
          d_daus = [abs(d.daughter(i).pdgId()) for i in range(d.numberOfDaughters())]
          if len(d_daus) != 2          : continue; 

          d_daus = set(d_daus)
          if d_daus != {333,211}       : continue; 

          #get pi
          pi = getDaughter(d,211) 
          #pi must have same charge as ds
          if pi.charge() != d.charge() : continue;

          #get phi
          phi = getDaughter(d,333)

          #we only want phi -> K K
          phi_daus = [abs(phi.daughter(i).pdgId()) for i in range(phi.numberOfDaughters())]
          if len(phi_daus) != 2        : continue;

          phi_daus = set(phi_daus)
          if phi_daus != {321}         : continue; 

          #last but not least, check that KK are opposite charge (must be!)
          if phi.daughter(0).charge() == phi.daughter(1).charge(): continue;

          #if we survived until here, this is a good ds
          has_good_ds_dau = True 
  
       
        for m in Mu:

          #keep only daughters
          if not isDaughter(b,m)        : continue;
   
          has_good_mu_dau = True 
        
        if has_good_ds_dau and has_good_mu_dau: 
          #this is a good b mom!
          good_Bs.append(b)
       
      if debug:
        for bs in good_Bs:
            print("------ good B IN THE EVENT -------")
            printDaughters(bs)


      #save the moms and their daughters
      for b in good_Bs:
        good_Bs_str.append(pdg_to_name[abs(b.pdgId())])

        b_daus = [pdg_to_name[abs(b.daughter(i).pdgId())] for i in range(b.numberOfDaughters())]
        good_Bs_decays_str.append(b_daus)

  del events
  #gc.collect() 
  #time.sleep(1)

  return good_Bs_str, good_Bs_decays_str



#pdb.set_trace()

#get events for every file ...
#for j,events in enumerate(event_list): 


good_Bs_str, good_Bs_decays_str = processFile(inputFiles,maxevents,debug)

#for j,f in enumerate(inputFiles):
#
#  print("processing file nr. ", j, " out of ", len(inputFiles))
#
#  good_Bs, good_Bs_decay = processFile(f,maxevents,debug)
#
#  #save the moms and their daughters
#  for b in good_Bs:
#    good_Bs_str.append(pdg_to_name[abs(b.pdgId())])
#
#    b_daus = [pdg_to_name[abs(b.daughter(i).pdgId())] for i in range(b.numberOfDaughters())]
#    good_Bs_decay_str.append(b_daus)


print("this file has ", len(good_Bs_str) , "B events")
with open(fout + "/B_moms/B_moms_chunk_" + str(chunk) + ".csv", 'a') as myfile:
  #myfile.write("# ---- File processed ----\n")
  wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
  for b in good_Bs_str:
    wr.writerow([b]) 

with open(fout + "/B_mom_decays/B_mom_decays_chunk_" + str(chunk) + ".csv", 'a') as myfile:
  #myfile.write("# ---- File processed ----\n")
  wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
  for decay in good_Bs_decays_str:
    wr.writerow([decay]) 

 

