from CRABClient.UserUtilities import config, ClientException
import yaml
import datetime
from fnmatch import fnmatch
from argparse import ArgumentParser

test = False 

date_time = datetime.date.today().strftime('%Y%m%d')

# create instace
config = config()

# set general parameters
config.section_('General')
config.General.transferOutputs = True        # transfer to T2
config.General.transferLogs    = True        # save logs
config.General.workArea        = date_time   # save logs at

# set in- and output data parameters
config.section_('Data')
if not test:
  config.Data.publication          = True         # save on the DAS, much easier for DIGI step
  config.Data.outputPrimaryDataset = 'hbInclusiveToDsPhiKKPi'         # save on the DAS, much easier for DIGI step
  #config.Data.outLFNDirBase        = '/store/user/pahwagne/' % date_time # destination on T2
  config.Data.splitting            = 'EventBased' # split via events (only option for MC) 
  config.Data.totalUnits           = 3000000000   # the total nr of to be produced events (mandatory for privateMC)
  config.Data.unitsPerJob          = 300000       # nr of produced events per job
else:
  # ONLY WHEN TESTING SINGLE FILE  
  config.Data.publication          = False        # dont save on the DAS
  config.Data.outLFNDirBase        = '/store/user/pahwagne/%s' % date_time # destination on T2
  config.Data.splitting            = 'EventBased'
  config.Data.totalUnits           = 500 
  config.Data.unitsPerJob          = 500 # the total nr of to be produced events (mandatory for privateMC)

# job settings
config.section_('JobType')
config.JobType.pluginName          = 'PrivateMC'   # running new MC production
config.JobType.psetName            =  '../GEN-SIM/hb/hb_cfg.py' #cmssw cfg file to run
config.JobType.eventsPerLumi       = 300 #100k events ~ 1000 lumi sections (->300k events ~3000 lumi sections), each with ~300 events 
config.JobType.maxJobRuntimeMin    = 2000  #in minutes, set job time to ~ 1.5 * default for data processing ( ~ 30h )


config.section_('User')
# specify output site
config.section_('Site')

config.Site.ignoreGlobalBlacklist   = True
config.Site.whitelist               = ['T2_CH_CSCS'] #run only in lugano
config.Site.storageSite             = 'T2_CH_CSCS'



