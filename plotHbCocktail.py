import ROOT
import argparse
import os
import sys
import yaml
from datetime import datetime
import matplotlib.pyplot as plt

import pandas as pd
import ast
import numpy as np
from collections import Counter

# parsing
parser = argparse.ArgumentParser()
parser.add_argument("--file",         required = True,     help = "filename")
args = parser.parse_args()

os.system(f"mkdir -p ./{args.file}/plots/")

#read the csv files

B_moms_csv       = [f for f in os.listdir(f"./{args.file}/B_moms/") if f.endswith(".csv")]
B_mom_decays_csv = [f for f in os.listdir(f"./{args.file}/B_mom_decays/") if f.endswith(".csv")]

chunks = len(B_moms_csv)

list_b_mom=[]
list_b_dec=[]

for i in range(chunks):

  try:
    df_b_mom = pd.read_csv(f"./{args.file}/B_moms/B_moms_chunk_{i}.csv", header = None)
    df_b_dec = pd.read_csv(f"./{args.file}/B_mom_decays/B_mom_decays_chunk_{i}.csv", header = None)
  except:
    print(f"Chunk {i} not found, skip it")
    continue;

  #convert to list
  list_b_mom.extend(df_b_mom[0].tolist())
  list_b_dec.extend(df_b_dec[0].apply(ast.literal_eval).tolist())

#now we have two lists, and we have to identify the decay uniquely

merged = []
for mom, dec in zip(list_b_mom,list_b_dec):
 
  
  #convert final state into set, such that order doesnt matter
  dec = set(dec)
  #sort it into a list
  dec = sorted(dec)
  #now build a tuple
  mom_and_dec = (mom, tuple(dec))

  merged.append(mom_and_dec)

#count total nr of events
ntot = len(merged)
ntot_wout_sig = 0


#this counts the occurance of each element
counted = Counter(merged)

#count everything except signals
for key,val in counted.items(): 
  if key != ('B_s0', ('D_s+', 'mu-', 'nu_mu')):
    ntot_wout_sig += val

#convert into percent
for key,val in counted.items():
  counted[key] = round(val/ntot * 100,4)

#occur = {}
#for s in merged_set:
#  np.count_nonzero(merged == s) / ntot
#


 
