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
 
  
  #convert final such that order doesnt matter
  #elements() returns an iterator, that can be turned into list etc. Multiplicity is kept!
  #use sorted to not care about order!
  dec = sorted(Counter(dec).elements())
  #now build a tuple
  mom_and_dec = (mom, tuple(dec))

  merged.append(mom_and_dec)

#count total nr of events
ntot = len(merged)
ntot_wout_sig = 0


#this counts the occurance of each element
counted = Counter(merged)
counted_wout_sig = {}
#count everything except signals
for key,val in counted.items(): 
  if key == ('B_s0', ('D_s+', 'mu-', 'nu_mu'))   : continue
  if key == ('B_s0', ('D_s+', 'nu_tau', 'tau-')) : continue
  if key == ('B_s0', ('D_s*+', 'mu-', 'nu_mu'))  : continue
  if key == ('B_s0', ('D_s*+', 'nu_tau', 'tau-')): continue
  ntot_wout_sig += val

#convert into percent
for key,val in counted.items():
  counted[key]          = round(val/ntot * 100,4)

  if key == ('B_s0', ('D_s+', 'mu-', 'nu_mu'))   : continue
  if key == ('B_s0', ('D_s+', 'nu_tau', 'tau-')) : continue
  if key == ('B_s0', ('D_s*+', 'mu-', 'nu_mu'))  : continue
  if key == ('B_s0', ('D_s*+', 'nu_tau', 'tau-')): continue

  counted_wout_sig[key] = round(val/ntot_wout_sig * 100,6)

#sort according to BR 
sorted_counts          = dict(sorted(counted.items(), key=lambda x: x[1]))
sorted_counts_wout_sig = dict(sorted(counted_wout_sig.items(), key=lambda x: x[1]))


#get keys only
sorted_keys          = [key[0] + " --> " + str(key[1]) for key in list(sorted_counts.keys())]
sorted_keys_wout_sig = [key[0] + " --> " + str(key[1]) for key in list(sorted_counts_wout_sig.keys())]
sorted_vals          = list(sorted_counts.values())
sorted_vals_wout_sig = list(sorted_counts_wout_sig.values())

#produce bar plot

# Plot using matplotlib
fig, ax = plt.subplots(figsize=(20, 200))
bars = ax.barh(sorted_keys, sorted_vals, height=1.0, align = "center")

ax.set_ylabel("Signal")
ax.tick_params(axis='y', labelsize=20) 
ax.tick_params(axis='x', labelsize=20) 
plt.subplots_adjust(left=0.4)  
plt.subplots_adjust(top=0.99, bottom=0.01)
ax.set_ylim(-0.5, len(sorted_keys) - 0.5)
ax.set_xlabel("Proportion in Cocktail [%]", fontsize=14)
ax.xaxis.set_label_position("top")

# Add value labels on top of each bar
ax.bar_label(bars, fmt='%.2f', padding=3, fontsize = 14)  # Adjust fmt and padding as needed

plt.savefig(f"./{args.file}/plots/hbCocktail.pdf")

plt.clf()
fig, ax = plt.subplots(figsize=(20, 200))
bars = ax.barh(sorted_keys_wout_sig, sorted_vals_wout_sig, height=1.0, align = "center")

ax.set_ylabel("Signal")
ax.tick_params(axis='y', labelsize=20) 
ax.tick_params(axis='x', labelsize=20) 
plt.subplots_adjust(left=0.4)  
plt.subplots_adjust(top=0.99, bottom=0.01)
ax.set_ylim(-0.5, len(sorted_keys_wout_sig) - 0.5)
ax.set_xlabel("Proportion in Cocktail [%]", fontsize=14)
ax.xaxis.set_label_position("top")

# Add value labels on top of each bar
ax.bar_label(bars, fmt='%.2f', padding=3, fontsize = 14)  # Adjust fmt and padding as needed

plt.savefig(f"./{args.file}/plots/hbCocktail_wout_sig.pdf")

