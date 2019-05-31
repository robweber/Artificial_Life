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
logArray = None

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

#return current running logFile
@webiopi.macro
def getLogs():
    global logArray
    return json.dumps(logArray)

#### WEB MACROS END HERE

def logLine(message,debug=False):
    global logArray
    global is_running

    if(debug):
        #if debug don't put in logArray
        webiopi.debug(message)
    else:
        #both print to log and logArray
        webiopi.info(message)

        if(is_running):
            logArray.append(message)

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
    global logArray

    #clear the logArray (python2 doesn't have clear() method)
    del logArray[:]

    #reset the next id number to total at start + 1
    settings.setValue(constants.NEXT_ID,settings.getValue(constants.NUM_LIFEFORMS_START) + 1)

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
    global logArray

    #load the settings file
    settings = Settings('/home/pi/Artificial_Life/')

    #setup the log array
    logArray = []
    
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
                    logLine('%d has expired' % Id)
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
                #check for any collisions with any other entities and return the id of an entity collided with if so
                colliderScope = collisionDetector(posList, posX, posY, Id)
                #get the count of total lifeforms currently active
                lifeFormTotalCount = len(iList)

                #if there has been a collision with another entity it will attempt to interact with the other entity
                if colliderScope:
                    #list variable for use later is cleared
                    transfers = []
                    #print information of the collision to screen
                    logLine('Collision detected: ' + str(Id) + ' collided with ' + str(colliderScope))
                    #call the randomise direction function for the entity
                    holder[Id].randomiseDirection()

                    #if the aggression factor is below 850 the lifeform will attempt to breed with the one it collided with
                    if holder[Id].aggressionFactor < 850:
                        logLine('Breeding %d with %d' % (Id,colliderScope))

                        #the breeding will attempt only if the current lifeform count is not above the population limit
                        if lifeFormTotalCount < popLimit:
                            #generate 2 random numbers for x and y positions of the new entity
                            posXGen, posYGen = boardPositionGenerator()
                            #posXGen = random.randint(1, 8)
                            #posYGen = random.randint(1, 8)
              
                            #check for an entity at this position
                            for i in posList:
                                colliderScopeBirthConflicter = collisionDetector(posList, posXGen, posYGen, Id)     
                                if colliderScopeBirthConflicter:
                                    posXGen, posYGen = boardPositionGenerator()
                                    #posXGen = random.randint(1, 8)
                                    #posYGen = random.randint(1, 8)
                  
                                    #if the aggression factor is too low for the entity collided with and there is an entity at the current location its offspring wants to spawn, it will not do anything and no new entity will spawn
                                    if holder[colliderScope].aggressionFactor < 250:
                                        #print infromation and continue to next iteration of the loop
                                        logLine('Breeding failed')
                                        continue
                  
                                    #if the aggression factor is higher than the entity currently in place, the currently existing entity will be killed and replaced with the new offspring
                                    elif holder[colliderScope].aggressionFactor > holder[colliderScopeBirthConflicter].aggressionFactor:
                                        #call the kill entity function for the entity blocking the offspring
                                        iList = holder[colliderScopeBirthConflicter].killEntity(iList)
                                        #remove the killed entity from the position list so that it cant be collided with on the next iteration
                                        posList.remove([colliderScopeBirthConflicter, holder[colliderScopeBirthConflicter].matrixPositionX, holder[colliderScopeBirthConflicter].matrixPositionY])
                                        #append the lifeform to the list used by the main loop
                                        iList.append(settings.getValue(constants.NEXT_ID))
                                        #create a dictionary containing the instance id of the new class instance for the lifeform
                                        hUpdate = {settings.getValue(constants.NEXT_ID): lifeForm(settings.getValue(constants.NEXT_ID),maxAggro,maxTTL)}
                                        #update the list containing all of the instance ids of the main entity class
                                        holder.update(hUpdate)
                    
                                        #the below assigns all 3 lifeseeds with the potential to take the lifeseed from either parent (40% chance each), or whether a new random lifeseed will be inserted (20% chance), resulting in some genetic chaos to change offspring randomly
                                        transferOptions1 = [holder[Id].lifeSeed, holder[colliderScope].lifeSeed, genRandom()]
                                        transferOptions2 = [holder[Id].lifeSeed2, holder[colliderScope].lifeSeed2, genRandom()]
                                        transferOptions3 = [holder[Id].lifeSeed3, holder[colliderScope].lifeSeed3, genRandom()]
                    
                                        #print information to the console
                                        logLine('%d killed to make room for %d' % (colliderScopeBirthConflicter,settings.getValue(constants.NEXT_ID)))
                    
                                        #generate new lifeform with the chances of taking the information from each lifeseed or a totally new random seed, creating them at the x and y coords determined above
                                        generateLifeformAttribsSpark(settings.getValue(constants.NEXT_ID), int(np.random.choice(transferOptions1, 1, p=[0.4, 0.4, 0.2])), int(np.random.choice(transferOptions2, 1, p=[0.4, 0.4, 0.2])), int(np.random.choice(transferOptions3, 1, p=[0.4, 0.4, 0.2])), posXGen, posYGen)

                                        #update next id number
                                        settings.setValue(constants.NEXT_ID,settings.getValue(constants.NEXT_ID) + 1)
                                        #break the loop as no more needs to be done
                                        break
                  
                                    #if the aggression factor of the already existing entity is higher then the current entity will be killed and no offspring produced
                                    elif holder[colliderScope].aggressionFactor < holder[colliderScopeBirthConflicter].aggressionFactor:
                                        logLine('%d killed parent %d, breeding failed' % (colliderScopeBirthConflicter,colliderScope))
                                        iList = holder[colliderScope].killEntity(iList)
                                        posList.remove([colliderScope, holder[colliderScope].matrixPositionX, holder[colliderScope].matrixPositionY])
                                        #break the loop as no more needs to be done
                                        break
                
                                #if there is no entity in the place of the potential offspring the new entity will be created at the x and y coords determined above
                                else:
                                    logLine('%d created' % settings.getValue(constants.NEXT_ID))
                                    #add new lifeform to list
                                    iList.append(settings.getValue(constants.NEXT_ID))
                                    hUpdate = {settings.getValue(constants.NEXT_ID): lifeForm(settings.getValue(constants.NEXT_ID),maxAggro,maxTTL)}
                                    holder.update(hUpdate)
              
                                    #the below assigns all 3 lifeseeds with the potential to take the lifeseed from either parent (40% chance each), or whether a new random lifeseed will be inserted (20% chance), resulting in some genetic chaos to change offspring randomly
                                    transferOptions1 = [holder[Id].lifeSeed, holder[colliderScope].lifeSeed, genRandom()]
                                    transferOptions2 = [holder[Id].lifeSeed2, holder[colliderScope].lifeSeed2, genRandom()]
                                    transferOptions3 = [holder[Id].lifeSeed3, holder[colliderScope].lifeSeed3, genRandom()]
                  
                                    #generate new lifeform with the chances of taking the information from each lifeseed or a totally new random seed, creating them at the x and y coords determined above
                                    generateLifeformAttribsSpark(settings.getValue(constants.NEXT_ID), int(np.random.choice(transferOptions1, 1, p=[0.4, 0.4, 0.2])), int(np.random.choice(transferOptions2, 1, p=[0.4, 0.4, 0.2])), int(np.random.choice(transferOptions3, 1, p=[0.4, 0.4, 0.2])), posXGen, posYGen)

                                    #update the next ID number
                                    settings.setValue(constants.NEXT_ID,settings.getValue(constants.NEXT_ID) + 1)
                                    break
            
                        #if the current amount of lifeforms on the board is at the population limit or above then do nothing
                        elif lifeFormTotalCount >= popLimit:
                            continue

                    #if the entities aggression factor is above 850 it will attempt to kill the entity it has collided with instead of breed
                    elif holder[Id].aggressionFactor > 850:
                        #if the other entities aggression factor is lower it will be killed and removed from the main loops list of entities
                        if holder[colliderScope].aggressionFactor < holder[Id].aggressionFactor:
                            logLine('Entity %d killed' % colliderScope)
                            iList = holder[colliderScope].killEntity(iList)
                            posList.remove([colliderScope, holder[colliderScope].matrixPositionX, holder[colliderScope].matrixPositionY])
                        #if the other entities aggression factor is higher it will be kill the current entity and it will be removed from the main loops list of entities
                        elif holder[colliderScope].aggressionFactor > holder[Id].aggressionFactor:
                            logLine('Entity %d killed' % Id)
                            iList = holder[Id].killEntity(iList)
                            posList.remove([Id, holder[Id].matrixPositionX, holder[Id].matrixPositionY])
                        #if the aggression factor of both entities is identical they will reach a stalemate and simply bounce off each other
                        elif holder[colliderScope].aggressionFactor == holder[Id].aggressionFactor:
                            logLine('Neither entity killed')
                            continue
        elif not iList:
            logLine('Program done')
            changeRunning('false')
        #show LEDs
        unicorn.show()
        #sleep for the value set by the user
        webiopi.sleep(settings.getValue(constants.SECONDS_BETWEEN_LOOPS))
    else:
        #sleep for a bit and check again
        webiopi.sleep(5)

