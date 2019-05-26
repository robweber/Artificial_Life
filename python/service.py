import webiopi
import json
import sys
import random
import time
import os
import numpy as np
import unicornhat as unicorn
from operator import itemgetter

#do this to import local modules
module_path = '/home/pi/Artificial_Life/python'
if module_path not in sys.path:
   sys.path.append(module_path)

#import custom classes
import constants
from settings import Settings
from artificiallife import lifeForm

#### GLOBAL VARIABLES
is_running = False
settings = None
iList = None
holder = None

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

    response = {'message':'','is_running':is_running}

    if(is_running):
        response['message'] = 'Starting Artificial Life'
        setup_game() #startup the game variables here
    else:
        response['message'] = 'Stopping Artificial Life'

    return json.dumps(response)

#### WEB MACROS END HERE

#print the number of lifeforms currently on the board
def printLifeformNo(no):
    webiopi.info("Lifeforms: " + str(no))

#draw the position and colour of the current lifeform onto the board
def drawLEDS(x, y, r, g, b):
    unicorn.set_pixel(x, y, r, g, b)
    #unicorn.show()

#clear the unicorn hat led grid 
def clearLEDS():
    unicorn.clear()

#function used for generating a random number to be used as a seed, this is used to generate all 3 lifeseeds resulting in 1.e+36 possible types of lifeform
def genRandom():
    return random.randint(1, 1000000000000)

#function used to determine whether a lifeform is colliding with another currently on the board 
def collisionDetector(boardPositions, posX, posY, Id):
  
    #get the board positions for the current lifeform
    idX = posX
    idY = posY
  
    #clear lists that will be used to temporarily store x, y info for other lifeforms on the board, for comparison
    sItemX = ()
    sItemY = ()

    #for every item in the list of board positions perform a loop
    for item in boardPositions:
    
        #split the items in the sub-list into seperate variables for comparison
        sItemId = itemgetter(0)(item)
        sItemX = itemgetter(1)(item)
        sItemY = itemgetter(2)(item)

        #if the id of the lifeform in the position list matches the id of the lifeform currently being checked, then do nothing - to prevent lifeforms from colliding with themselves
        if sItemId == Id:
            continue
    
        #if the x and y positions match that of a lifeform that is currently on the position list then return the id of the lifeform it collided with
        elif idX == sItemX and idY == sItemY:
            return sItemId

#function for generating a new lifeform within the program      
def generateLifeformAttribsSpark(Id, lifeSeed, lifeSeed2, lifeSeed3, posXGen, posYGen):
    global holder
    holder[Id].sparkLife(lifeSeed, lifeSeed2, lifeSeed3, posXGen, posYGen)  

#function that assign lifeforms ids from the total number recieved by the function and puts them in a list
def assignClasses(total):
  
    iList = []
    for i in range(total):
        i += 1
        iList.append(i)
  
    return (iList)
  
def boardPositionGenerator():
    posXGen = random.randint(0, 7)
    posYGen = random.randint(0, 7)
    return posXGen, posYGen

def setup_game():
    global iList
    global holder
    global settings

    #obtain lifeform id list from the above function  
    iList = assignClasses(settings.getValue(constants.NUM_LIFEFORMS_START))
    #assign all the ids into class instances for each lifeform
    holder = {Id: lifeForm(Id,settings.getValue(constants.MAX_AGRESSION),settings.getValue(constants.MAX_TTL)) for Id in iList}

    #for each id in the list of all lifeform ids assign a random x and y number for the position on the board and create the new lifeform with random seeds for each lifeseed generation
    for Id in iList:
  
        posXGen, posYGen = boardPositionGenerator()
        #posXGen = random.randint(1, 8)
        #posYGen = random.randint(1, 8)
        generateLifeformAttribsSpark(Id, genRandom(), genRandom(), genRandom(), posXGen, posYGen)

#### SETUP - called at webiopi startup
def setup():
    global settings

    #load the settings file
    settings = Settings('/home/pi/Artificial_Life/')
    
    #unicorn hat setup    
    unicorn.set_layout(unicorn.AUTO)
    unicorn.brightness(0.5)
    unicorn.rotation(0)
    unicorn.brightness(0.5)

    webiopi.info('setup complete')

#### LOOP - main webiopi loop
def loop():
    global is_running
    global settings
    global iList
    global holder

    if(is_running):
        webiopi.info("program is running")

        #get the settings from the settings class
        lifeFormTotal = settings.getValue(constants.NUM_LIFEFORMS_START)
        popLimit = settings.getValue(constants.MAX_LIFEFORMS)
        maxTTL = settings.getValue(constants.MAX_TTL)
        maxAggro = settings.getValue(constants.MAX_AGRESSION)

        clearLEDS()
        posList = []

        if iList:
            for Id in iList:  
                #clear colliderscope variable to make sure its fresh from data from the last iteration
                colliderScope = ()
                #call the movement function for the lifeform
                holder[Id].movement()
                #call expiry function for current lifeform and update the list of lifeforms
                iList = holder[Id].expireEntity(iList)
                #if the lifeform has expired then skip the loop as we dont want to continue processing an entity which is no longer on the board
                if Id not in iList:
                    continue
                #print stats of current lifeform to console
                holder[Id].getStats()
                #assign variables from information about lifeform for use later
                posX = holder[Id].matrixPositionX
                posY = holder[Id].matrixPositionY
                colR = holder[Id].redColor
                colG = holder[Id].greenColor
                colB = holder[Id].blueColor
                #call function to draw leds with the current lifeforms x and y and r g b data, as well as the current layer
                drawLEDS(posX, posY, colR, colG, colB)
                #append the lifeforms id and x and y location to to the position list to be used by the collisiondetector
                posList.append([Id, posX, posY])
        elif not iList:
            webiopi.info('Program done')
            changeRunning('false')
        #show LEDs
        unicorn.show()
        #sleep for the value set by the user
        webiopi.sleep(settings.getValue(constants.SECONDS_BETWEEN_LOOPS))
    else:
        webiopi.info("program is not running")
        webiopi.sleep(5)

