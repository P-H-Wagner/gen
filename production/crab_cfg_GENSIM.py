from CRABClient.UserUtilities import config, ClientException
import yaml
import datetime
from fnmatch import fnmatch
from argparse import ArgumentParser

test = True 

date_time = datetime.date.today().strftime('%Y%b%d')

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
  config.Data.publication        = False        # dont save on the DAS
  config.Data.outLFNDirBase      = '/store/user/pahwagne/%s' % date_time # destination on T2
  config.Data.splitting          = 'EventBased' # split via events (only option for MC) 
  config.Data.totalUnits         = 1000000      # the total nr of to be produced events (mandatory for privateMC)
  config.Data.unitsPerJob        = 1000         # nr of produced events per job
else:
  # ONLY WHEN TESTING SINGLE FILE
  config.Data.publication        = False        # dont save on the DAS
  config.Data.outLFNDirBase      = '/store/user/pahwagne/%s' % date_time # destination on T2
  config.Data.splitting          = 'EventBased'
  config.Data.totalUnits         = 1000
  config.Data.unitsPerJob        = 100          # the total nr of to be produced events (mandatory for privateMC)

# job settings
config.section_('JobType')
config.JobType.pluginName       = 'PrivateMC'   # running new MC production
config.JobType.psetName         =  '../GEN-SIM/hb/hb_cfg.py' #cmssw cfg file to run
#config.JobType.maxJobRuntimeMin = 1972  #set job time to 1.5 * default for data processing ( ~ 30h, i.e. 3h per data file, since we submit in batches of 10)


config.section_('User')
# specify output site
config.section_('Site')
#config.Site.whitelist   = ['T2_CH_CSCS'] #run only in lugano
config.Site.storageSite = 'T2_CH_CSCS'



