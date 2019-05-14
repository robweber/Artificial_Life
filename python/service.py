import webiopi
import json

#do this to import local modules
module_path = '/home/pi/Git/betabrite-sign/python'
if module_path not in sys.path:
   sys.path.append(module_path)

#import custom classes
import constants
from settings import Settings

#global variables
is_running = False
settings = None

#web macros
@webiopi.macro
def saveSettings(numStart,timeDelay,maxNum,maxTTL,maxAgression):
    global settings
    webiopi.info('saving')

    #save the settings
    settings.setValue(constants.NUM_LIFEFORMS_START,numStart)
    settings.setValue(constants.SECONDS_BETWEEN_LOOPS,timeDelay)
    settings.setValue(constants.MAX_LIFEFORMS,maxNum)
    settings.setValue(constants.MAX_TTL,maxTTL)
    settings.setValue(constants.MAX_AGRESSION,maxAgression)

    return json.dumps({"message":"Settings Saved"})

@webiopi.macro
def getSettings():
    global settings

    return json.dumps(settings.getAllValues())

def setup():
    global settings

    #load the settings file
    settings = Settings('/home/pi/Git/Artificial_Life')
    
    webiopi.info('setup complete')

def loop():
    webiopi.info('loop')


    #sleep for 5 seconds
    webiopi.sleep(5)
