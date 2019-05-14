import webiopi
import json

#global variables
is_running = False

#web macros
@webiopi.macro
def saveSettings(numStart,timeDelay,maxNum,maxTTL,maxAgression):
    webiopi.info('saving')

    return json.dumps({"message":"Settings Saved"})

def setup():
    webiopi.info('setup here')

def loop():
    webiopi.info('loop')


    #sleep for 5 seconds
    webiopi.sleep(5)
