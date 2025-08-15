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
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('channel')
args = parser.parse_args()

#to process
if args.channel == "all":
  fragments = ["signals","Bs","B+","B0","LambdaB"]
else:
  fragments = [args.channel]


# We measured to be able to produce:  9 events / second -> dont use that
# On the standard queue we only hat 2.5 events / second!!!!!!

# short lane = 800, standart = 500, long = 200

# For a first test within short queue: 30 minutes == 1800s --> 1800s * 9ev/s = 16'200 events
# So lets create 800 jobs (the max for every user), each producing 15'000 events
# Lets do not create Bc (special case), so we have 4 mothers -> 800/4 = 200 jobs per mother
# Given that we run on 8 threads, lets submit 200/8 = 25 jobs per mother with 15000 events

#For the big submit we submit to the standard queue. From the short test above we've seen that its safer to
#do the calculation with 4ev/s. We have 7h = 25200s, thus we have 4ev/s * 25200s = 100800 events in each sample. 
#on standard we have 500 jobs -> take 100 for every of the 4 mothers = use 400 jobs. Since we have 8 cores, we assign 100/8 = 12 jobs for each mother 

#Event throughout for MC without filter (for hammer) is 2ev/s


njobs = 1 #30
events_per_job =  5000#5000
queue = 'standard' ; time = 240 #720 
#queue = 'short'   ; time = 60
#queue = 'short'    ; time = 45

#get date and time
now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

#fragments to produce
print("Preparing folders for {0} decays".format(fragments))

for fragment in fragments:

  out_dir          = "{0}_fragment_{1}".format(fragment,dt_string)

  template_cfg     = "{0}_cfg_template.py".format(fragment)
  template_fileout = "{0}_fragment_{1}.root".format(fragment,dt_string)
  
  ##########################################################################################
  ##########################################################################################
  
  # make output dir if non-existent
  os.makedirs("/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/"+out_dir)
  os.makedirs("./"+out_dir)
  os.makedirs(out_dir + '/logs')
  os.makedirs(out_dir + '/errs')


  #loop over jobs
  for ijob in range(njobs):

    tmp_cfg = template_cfg.replace("cfg_template", "cfg_chunk{0}".format(ijob))
    tmp_fileout = template_fileout.replace("fragment","fragment_chunk{0}".format(ijob))
    
    #input file
    fin = open( "config_files/" + template_cfg, "rt") 

    #output file to write the result to
    fout = open("{0}/{1}".format(out_dir, tmp_cfg), "wt")

    #for each line in the input file
    for line in fin:
        #read replace the string and write to output file
        if "HOOK_FIRST_LUMI" in line: fout.write(line.replace("HOOK_FIRST_LUMI", "%d" %ijob))
        elif "HOOK_MAX_EVENTS" in line: fout.write(line.replace("HOOK_MAX_EVENTS", "%d" %events_per_job))
        #elif "HOOK_FILE_OUT"   in line: fout.write(line.replace("HOOK_FILE_OUT"  , "/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/test.root")) #for testing

        elif "HOOK_FILE_OUT"   in line: fout.write(line.replace("HOOK_FILE_OUT"  , "/scratch/pahwagne/{0}/{1}".format(out_dir, tmp_fileout)))
        else: fout.write(line)
    #close input and output files
    fout.close()
    fin.close()

    to_write = '\n'.join([
        '#!/bin/bash',
        # --- create scratch dir and create temp .sh file in scratch ---
        'mkdir -p /scratch/pahwagne/{scratch_dir}',
        'payload=/scratch/pahwagne/{scratch_dir}/apptainer-payload-{xxx}.sh',
        # --- write into temp ---
        'cat > "$payload" << EOF',
        'cd /work/pahwagne/gen/CMSSW_10_6_37/src/rds/gen', 
        'source $VO_CMS_SW_DIR/cmsset_default.sh', 
        'export SCRAM_ARCH=slc7_amd64_gcc700', #export new arch
        'cmsenv',
        'echo ">>>> cmsenv activated"',
        'cd {dir}',
        'scramv1 runtime -sh',
        'cmsRun {cfg}',
        'xrdcp /scratch/pahwagne/{scratch_dir}/{fout} root://t3dcachedb03.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/pahwagne/miniAOD/{se_dir}/{fout}',
        'EOF',
        # --- close tmp file ---
        'echo "printing oayload content:"',
        'cat /scratch/pahwagne/{scratch_dir}/apptainer-payload-{xxx}.sh',
        'rm /scratch/pahwagne/{scratch_dir}/{fout}',
        'echo ">>>> Done, launching cfg "',

        # --- make payload executable and run it in el7 singularity ---

        'chmod u+x "$payload"',
        '/cvmfs/cms.cern.ch/common/cmssw-el7  --bind /scratch,/work --command-to-run $payload'

    ]).format(
        dir           = '/'.join([os.getcwd(), out_dir]), 
        scratch_dir   = out_dir, 
        cfg           = tmp_cfg, 
        se_dir        = out_dir,
        fout          = tmp_fileout,
        xxx           = ijob
        )

    with open("%s/submitter_chunk%d.sh" %(out_dir, ijob), "wt") as flauncher: 
        flauncher.write(to_write)
    
    command_sh_batch = ' '.join([
        'sbatch', 
        '-p %s'%queue, 
        '--account=t3', 
        #'--mem=1800M',
        '-o %s/logs/chunk%d.log' %(out_dir, ijob),
        '-e %s/errs/chunk%d.err' %(out_dir, ijob), 
        '--job-name=%s' %out_dir, 
        '--time=%d'%time,
        #'--cpus-per-task=8', 
        '%s/submitter_chunk%d.sh' %(out_dir, ijob), 
    ])

    print(command_sh_batch)
    os.system(command_sh_batch)
    
    
