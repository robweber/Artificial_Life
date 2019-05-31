import random

#the main class that handles each lifeforms initialisation, movement, colour, expiry and statistics
class lifeForm(object):
  
    #standard class initialisation
    def __init__(self, Id,globalAggression,globalTTL):
        self.Id = Id
        self.globalAggression = globalAggression
        self.globalTTL = globalTTL
        self.lifeSeed = 0
        self.lifeSeed2 = 0
        self.lifeSeed3 = 0
  
    #when this function is called it gives the lifeform of the class instance its properties from the random numbers inserted into it
    def sparkLife(self, seed, seed2, seed3, startX, startY):
        self.lifeSeed = seed
        self.lifeSeed2 = seed2
        self.lifeSeed3 = seed3
        #lifeseed 1 controls the random number generation for the green colour, maximum aggression factor starting direction and maximum possible lifespan
        random.seed(self.lifeSeed)
        self.greenColor = random.randint(1, 255)
        self.maxAggressionFactor = random.randint(1, self.globalAggression)
        self.direction = random.randint(1, 9)
        self.maxLife = random.randint(1, self.globalTTL)
        #lifeseed 2 controls the random number generation for the red colour, aggression factor between 0 and the maximum from above as well as the time the entity takes to change direction
        random.seed(self.lifeSeed2)
        self.aggressionFactor = random.randint(0, self.maxAggressionFactor)   
        self.redColor = int((float(self.aggressionFactor) / float(self.globalAggression)) * 255) #color is a function of how aggressive the entity is as a percentage of total reddness (ie, more aggressive is more red)
        self.timeToMove = random.randint(1, 25)
        self.timeToMoveCount = self.timeToMove
        #lifeseed 3 controls the random number generation for the blue colour, and time to live between 0 and the maximum from above
        random.seed(self.lifeSeed3)
        self.timeToLive = random.randint(0, self.maxLife)
        self.blueColor = int((float(self.timeToLive) / float(self.globalTTL)) * 255) #color is a function of total lifespan as a percentage of max lifespan (ie, longer life is bluer color)
        self.timeToLiveCount = self.timeToLive
        #reset the global random seed
        random.seed()
    
        #set the starting location of the lifeform from the x and y positions passed into the function
        self.matrixPositionX = startX
        self.matrixPositionY = startY

    #when called this function will display the statistics of the current lifeform in the main loop 
    def getStats(self):
        print ('ID: ' + str(self.Id))
        print ('Seed 1: ' + str(self.lifeSeed))
        print ('Seed 2: ' + str(self.lifeSeed2))
        print ('Seed 3: ' + str(self.lifeSeed3))
        print ('Direction: ' + str(self.direction))
        print ('Time to move total: ' + str(self.timeToMove))
        print ('Time to next move: ' + str(self.timeToMoveCount))
        print ('Total lifetime: ' + str(self.timeToLive))
        print ('Time left to live: ' + str(self.timeToLiveCount))
        print ('Aggression Factor: ' + str(self.aggressionFactor))
        print ('Position X: ' + str(self.matrixPositionX))
        print ('Position Y: ' + str(self.matrixPositionY))
        print ('Color: ' + 'R-' + str(self.redColor) + ' G-' + str(self.greenColor) + ' B-' + str(self.blueColor) + '\n')
  
    #this function will move the entity in its currently set direction (with 8 possible directions), if it hits the edge of the board it will then assign a new random direction to go in, this function also handles the time to move count which when hits 0 will select a new random direction for the entity regardless of whether it has hit the edge of the board or another entity
    def movement(self):
    
        #if the edge of the board is not hit and direction is '1' then move the entity up the X axis by 1, if it has hit the edge of the board its direction is randomised by the randomisedirection function being called for the entity
        if self.direction == 1:
            if self.matrixPositionX < 7:
                self.matrixPositionX += 1
            else:
                self.direction = self.randomiseDirection()
    
        #if the edge of the board is not hit and direction is '2' then move the entity down the X axis by 1, if it has hit the edge of the board its direction is randomised by the randomisedirection function being called for the entity   
        if self.direction == 2:
            if self.matrixPositionX > 0:
                self.matrixPositionX -= 1
            else:
                self.direction = self.randomiseDirection()
        
        #if the edge of the board is not hit and direction is '3' then move the entity up the Y axis by 1, if it has hit the edge of the board its direction is randomised by the randomisedirection function being called for the entity   
        if self.direction == 3:
            if self.matrixPositionY < 7:
                self.matrixPositionY += 1
            else:
                self.direction = self.randomiseDirection()
    
        #if the edge of the board is not hit and direction is '4' then move the entity down the Y axis by 1, if it has hit the edge of the board its direction is randomised by the randomisedirection function being called for the entity   
        if self.direction == 4:
            if self.matrixPositionY > 0:
                self.matrixPositionY -= 1
            else:
                self.direction = self.randomiseDirection()

        #if the edge of the board is not hit and direction is '5' then move the entity up the X and Y axis by 1, if it has hit the edge of the board its direction is randomised by the randomisedirection function being called for the entity
        if self.direction == 5:
            if self.matrixPositionX < 7 and self.matrixPositionY < 0:
                self.matrixPositionX += 1
                self.matrixPositionY += 1
            else:
                self.direction = self.randomiseDirection()

        #if the edge of the board is not hit and direction is '6' then move the entity down the X and Y axis by 1, if it has hit the edge of the board its direction is randomised by the randomisedirection function being called for the entity       
        if self.direction == 6:
            if self.matrixPositionX > 0 and self.matrixPositionY > 0:
                self.matrixPositionX -= 1
                self.matrixPositionY -= 1
            else:
                self.direction = self.randomiseDirection()

        #if the edge of the board is not hit and direction is '7' then move the entity down the X axis and up Y axis by 1, if it has hit the edge of the board its direction is randomised by the randomisedirection function being called for the entity       
        if self.direction == 7:
            if self.matrixPositionY < 7 and self.matrixPositionX > 0:
                self.matrixPositionX -= 1
                self.matrixPositionY += 1
            else:
                self.direction = self.randomiseDirection()

         #if the edge of the board is not hit and direction is '8' then move the entity up the X axis and down Y axis by 1, if it has hit the edge of the board its direction is randomised by the randomisedirection function being called for the entity           
        if self.direction == 8:
            if self.matrixPositionY > 0 and self.matrixPositionX < 7:
                self.matrixPositionX += 1
                self.matrixPositionY -= 1
            else:
                self.direction = self.randomiseDirection()
    
        #if the direction is '9' do not move the entity   
        elif self.direction == 9:
            self.matrixPositionX = self.matrixPositionX
            self.matrixPositionY = self.matrixPositionY
    
        #minus 1 from the time to move count until it hits 0, at which point the entity will change direction from the randomisedirecion function being called
        if self.timeToMoveCount > 0:
            self.timeToMoveCount -= 1
        elif self.timeToMoveCount <= 0:
            self.timeToMoveCount = self.timeToMove
            self.direction = self.randomiseDirection()
      
    #when called this function with select a random new direction for the lifeform that is not the direction it is already going    
    def randomiseDirection(self):
    
        r = range(1,self.direction) + range(self.direction+1, 10)
        return random.choice(r)
  
    #this function counts down a lifeforms time to live from its full lifetime assigned to it when a lifeforms time to live hits zero remove it from the list of lifeforms and set the colours to 0, 0, 0
    def expireEntity(self, iListIn):
    
        if self.timeToLiveCount > 0:
            self.timeToLiveCount -= 1
            return (iListIn)
        elif self.timeToLiveCount <= 0:
            self.redColor = 0
            self.greenColor = 0
            self.blueColor = 0
            iListIn.remove(self.Id)
            return (iListIn)
  
    #function to call for erasing an entity from the board as well as the main list for lifeforms
    def killEntity(self, iListIn):
        self.redColor = 0
        self.greenColor = 0
        self.blueColor = 0
        iListIn.remove(self.Id)
        return (iListIn)
      
    #function to call for erasing an entity from the board by fading it away as well as removing from the main list for lifeforms
    def fadeEntity(self, iListIn):
        for c in range(0, 255):
            if (self.redColor > 0):
                self.redColor -= 1
            if (self.greenColor > 0):
                self.greenColor -= 1
            if (self.blueColor > 0):
                self.blueColor -= 1
            unicorn.set_pixel(self.matrixPositionX, self.matrixPositionY, self.redColor, self.greenColor, self.blueColor)
            unicorn.show()
        iListIn.remove(self.Id)
        return (iListIn)
    
