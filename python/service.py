import webiopi
import json
import sys

#do this to import local modules
module_path = '/home/pi/Artificial_Life/python'
if module_path not in sys.path:
   sys.path.append(module_path)

#import custom classes
import constants
from settings import Settings

#### GLOBAL VARIABLES
is_running = False
settings = None

#### WEB MACROS START HERE

#save settings rest call
@webiopi.macro
def saveSettings(numStart,timeDelay,maxNum,maxTTL,maxAgression):
    global settings
    webiopi.info('saving settings')

    #save the settings
    settings.setValue(constants.NUM_LIFEFORMS_START,numStart)
    settings.setValue(constants.SECONDS_BETWEEN_LOOPS,timeDelay)
    settings.setValue(constants.MAX_LIFEFORMS,maxNum)
    settings.setValue(constants.MAX_TTL,maxTTL)
    settings.setValue(constants.MAX_AGRESSION,maxAgression)

    return json.dumps({"message":"Settings Saved"})

#get all settings rest call
@webiopi.macro
def getSettings():
    global settings

    return json.dumps(settings.getAllValues())

#check if the program is running
@webiopi.macro
def checkRunning():
    global is_running

    return json.dumps({"is_running":is_running})

#changes program running status
@webiopi.macro
def changeRunning(action):
    global is_running
    is_running = (True if action == 'true' else False)
    webiopi.info(action)
    response = {'message':'','is_running':is_running}

    if(action):
        response['message'] = 'Starting Artificial Life'
    else:
        response['message'] = 'Stopping Artificial Life'

    return json.dumps(response)

#### WEB MACROS END HERE

#### SETUP - called at webiopi startup
def setup():
    global settings

    #load the settings file
    settings = Settings('/home/pi/Artificial_Life/')
    
    webiopi.info('setup complete')

#### LOOP - main webiopi loop
def loop():
    global is_running
    
    if(is_running):
        webiopi.info("program is running")
    else:
        webiopi.info("program is not running")

    #sleep for 5 seconds
    webiopi.sleep(5)
