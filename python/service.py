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

#puts the program in running mode
@webiopi.macro
def startProgram():
    global is_running
    is_running = True

    return json.dumps({"message":"Starting Artificial Life"})

#stops the program, if currently running
@webiopi.macro
def stopProgram():
    global is_running
    is_running = False

    return json.dumps({"message":"Stopping Artificial Life"})

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
