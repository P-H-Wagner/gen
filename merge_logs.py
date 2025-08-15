import numpy as np
import argparse
import os
import re

#Define command line inputs
parser = argparse.ArgumentParser(description='Produce one logger from all chunks')
parser.add_argument('--date_and_time'        , dest='date_and_time'   , required='True'  , type=str)
parser.add_argument('mom')
#parser.add_argument('--output_file'       , dest='output_file'  , required='True'  , type=str)
args = parser.parse_args()

date_and_time = args.date_and_time
#output_file = args.output_file

home = "/work/pahwagne/gen/CMSSW_10_6_37/src/rds/gen/"
dirs = os.listdir(home)

if args.mom == "all":
  mothers = ["Bc+","Bs","B0","B+","LambdaB"]
else:
  mothers = [args.mom]


total_log = ""

for imom in mothers:
    for idir in dirs:

        if idir.endswith(date_and_time) and idir.startswith(imom):
            #correct date and time, extract the mother
            #get logs and errs
            logs = os.listdir(home+idir+"/logs")
            errs = os.listdir(home+idir+"/errs")
            #errs = ["chunk0.err","chunk1.err","chunk2.err","chunk3.err"]

            totaljobcpu = 0
            totaljobtime = 0
            passedevents = 0
            producedevents = 0
            throughput = 0  
            crosssection = 0
     
            n_err = 0
 
            failed_chunks = 0

            for err in errs:


                print("Reading file: {0}".format(err))                

                try:
                  with open(home+idir+"/errs/"+err) as infile:
  
                      last_lines = infile.readlines() [-100:]
                      if "CANCELLED AT" in last_lines[-1]: continue #skip job which were cancelled or empty files
  
                      # if we reach this point, the file is not empty :)
                      n_err += 1
                      counter = 0
                      total_jobs = []
                      for line in last_lines:
                          counter += 1
                          if 'Total job:' in line:
                              #print("here")          
                              numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
                              rx = re.compile(numeric_const_pattern, re.VERBOSE)
                              total_jobs.append(rx.findall(line))
                              #for i in line.split(): 
                              #    if i.isdigit(): total_job += total_job+i  
                              #total_jobs.append(total_job)
                              #print(total_jobs) 
                          if 'Filter efficiency (event-level)' in line:
                              numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
                              rx = re.compile(numeric_const_pattern, re.VERBOSE)
                              events = rx.findall(line)
      
                          if 'Event Throughput' in line:
                              numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
                              rx = re.compile(numeric_const_pattern, re.VERBOSE)
                              speed = rx.findall(line)
   
                          if 'After filter: final cross section' in line:
                              numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
                              rx = re.compile(numeric_const_pattern, re.VERBOSE)
                              cross = rx.findall(line)

                  #print(err)
                  #print(total_jobs) 
                  totaljobtime += float(total_jobs[0][0])    
                  totaljobcpu += float(total_jobs[1][0])    
                  passedevents += float(events[0])    
                  producedevents += float(events[1])    
                  throughput += float(speed[0])
                  crosssection += float(cross[0])               

                except: 
                  print("Chunk failed!")
                  failed_chunks += 1

            pnfs = '/pnfs/psi.ch/cms/trivcat/store/user/pahwagne/{0}_fragment_{1}'.format(imom,date_and_time)
            #get size of whole miniAOD folder for mother imom
            size = sum(os.path.getsize(pnfs + '/' + f) for f in os.listdir(pnfs)) /1000.0 #in MB

            if passedevents < 1:
              size_per_event = 0.
            else:
              size_per_event = int(size/passedevents + 1)
 
            to_write = [
            "------------------ {0} log --------------------- \n ".format(imom),    
            "Average job time:                           {0} s \n".format(totaljobtime/n_err),
            "Average job cpu:                            {0} s \n".format(totaljobcpu/n_err),
            "CPU efficiency:                             {0} % \n".format(round((totaljobcpu*100) / (8*totaljobtime),2)),

            "Total number of events which passed filter: {0}  \n".format(int(passedevents)),
            "Total number of events:                     {0}  \n".format(int(producedevents)),
            "Filter efficiency:                          {0}  \n".format(passedevents/producedevents),
            "Average cross section after filter:         {0} pb \n".format(crosssection/n_err),

            "Size of all miniAODs on disk                {0} KB  \n".format(int(size+1)), 
            "Size per event                              {0} KB  \n".format(size_per_event), 
            "Event throughput:                           {0} ev/s \n".format(round(throughput/n_err,2)),
            "Events per lumi section:                    {0} \n".format(int(8*3600*1*passedevents*throughput/(producedevents*n_err))),


            "To reach a lumi of 10 fb^-1 we need at least {0} events for {1}\n".format(int((10 * crosssection* 1000/n_err) + 1),imom),

            "Failed job chunks in log reading:           {0} \n".format(int(failed_chunks))]

            to_write = ''.join(to_write)
            total_log += to_write 

print(total_log)

with open("/work/pahwagne/gen/CMSSW_10_6_37/src/rds/gen/total_logs/log_{0}.txt".format(date_and_time), "wt") as flauncher:
    flauncher.write(total_log)



