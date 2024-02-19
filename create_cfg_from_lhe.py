'''
Cambia il rng seed!
https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideEDMRandomNumberGeneratorService
https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideFastSimRandNumGen

from IOMC.RandomEngine.RandomServiceHelper import  RandomNumberServiceHelper
randHelper =  RandomNumberServiceHelper(process.RandomNumberGeneratorService)
randHelper.populate()
process.RandomNumberGeneratorService.saveFileName =  cms.untracked.string("RandomEngineState.log")

multihtread jobs
https://wiki.chipp.ch/twiki/bin/view/CmsTier3/CPUExampleForUsingMultipleProcessors%28threads%29OnASinglePhysicalComputer

'''
import os
from glob import glob
from datetime import datetime
import sys

# short lane = 800, standart = 500, long = 200
# Bc speed: 3.5ev/s

njobs = 60
events_per_job = 40000
queue = 'standard'; time = 720 
#queue = 'short'   ; time = 60
# queue = 'long'    ; time = 10080

#get date and time
now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

# get root files produced from lhe files by cmsDriver.py command (the first one):
# https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_setup/BPH-RunIISummer20UL18pLHEGEN-00082
# riccardo did this for us :)
pnfs ="/pnfs/psi.ch/cms/trivcat/store/user/"
trees = os.listdir(pnfs+"manzoni/RJPsi_Bc_LHEGEN_11oct20_v3")
core = trees[0][0:-7]

# one job for every tree
if njobs < 0: njobs = len(trees) 

# this program does the 2nd cmsdriver command, i.e. get Gen compatible format from root file

# lhegen files at:
# https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=BPH-RunIISummer20UL18pLHEGEN-00082&page=0&shown=127

# fragments to produce
fragments = ["Bc+"]  

for fragment in fragments:

  out_dir          = "{0}_fragment_{1}".format(fragment,dt_string)
  template_cfg     = "{0}_cfg_template.py".format(fragment)
  template_fileout = "{0}_fragment_{1}.root".format(fragment,dt_string)
  
  ##########################################################################################
  ##########################################################################################
  
  # make output dir if non-existent
  os.makedirs(pnfs + "pahwagne/"+out_dir)
  os.makedirs("./"+out_dir)
  os.makedirs(out_dir + '/logs')
  os.makedirs(out_dir + '/errs')


  #loop over jobs
  for ijob in range(njobs):
    tree = core + "{0}.root".format(ijob)
    print(ijob)
    print(tree)
    tmp_cfg = template_cfg.replace("cfg_template", "cfg_chunk{0}".format(ijob))
    tmp_fileout = template_fileout.replace("fragment","fragment_chunk{0}".format(ijob))
    
    #input file
    fin = open("/work/pahwagne/CMSSW_10_6_37/src/cfg_from_cff/"+template_cfg, "rt") # the real deal

    #output file to write the result to
    fout = open("{0}/{1}".format(out_dir, tmp_cfg), "wt")

    #for each line in the input file
    for line in fin:
        #read replace the string and write to output file
        if "HOOK_FIRST_LUMI" in line: fout.write(line.replace("HOOK_FIRST_LUMI", "%d" %ijob)) #such that different events get different event number for every chunk! 
        elif "HOOK_MAX_EVENTS" in line: fout.write(line.replace("HOOK_MAX_EVENTS", "%d" %events_per_job))
        #elif "HOOK_FILE_OUT"   in line: fout.write(line.replace("HOOK_FILE_OUT"  , "/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/test.root")) #for testing
        elif "HOOK_FILE_IN"    in line: fout.write(line.replace("HOOK_FILE_IN"  ,pnfs + "manzoni/RJPsi_Bc_LHEGEN_11oct20_v3/" + tree))
        elif "HOOK_FILE_OUT"   in line: fout.write(line.replace("HOOK_FILE_OUT"  , "/scratch/pahwagne/{0}/{1}".format(out_dir, tmp_fileout)))
        else: fout.write(line)
    #close input and output files
    fout.close()
    fin.close()

    to_write = '\n'.join([
        '#!/bin/bash',
        'cd {dir}',
        'scramv1 runtime -sh',
        'mkdir -p /scratch/pahwagne/{scratch_dir}',
        'ls /scratch/pahwagne/',
        'cmsRun {cfg}',
        'xrdcp /scratch/pahwagne/{scratch_dir}/{fout} root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/pahwagne/{se_dir}/{fout}',
        'rm /scratch/pahwagne/{scratch_dir}/{fout}',
        '',
    ]).format(
        dir           = '/'.join([os.getcwd(), out_dir]), 
        scratch_dir   = out_dir, 
        cfg           = tmp_cfg, 
        se_dir        = out_dir,
        fout          = tmp_fileout
        )

    with open("%s/submitter_chunk%d.sh" %(out_dir, ijob), "wt") as flauncher: 
        flauncher.write(to_write)
    
    command_sh_batch = ' '.join([
        'sbatch', 
        '-p %s'%queue, 
        '--account=t3', 
        '--mem=3000M',
        '-o %s/logs/chunk%d.log' %(out_dir, ijob),
        '-e %s/errs/chunk%d.err' %(out_dir, ijob), 
        '--job-name=%s' %out_dir, 
        '--time=%d'%time,
        '--cpus-per-task=8', 
        '%s/submitter_chunk%d.sh' %(out_dir, ijob), 
    ])

    print(command_sh_batch)
    os.system(command_sh_batch)
    
    
