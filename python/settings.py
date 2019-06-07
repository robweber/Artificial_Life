import json
import os
from shutil import copyfile

class Settings:
    jsonObject = None
    jsonFile = None
	
    def __init__(self,filePath,fileName='settings'):
      self.jsonFile = filePath + 'data/' + fileName + '.json'

	    #check the settings file exists
      if(not os.path.isfile(self.jsonFile)):
	      #copy the default
        copyfile(filePath + 'data/' + fileName + '_default.json',self.jsonFile)

      self._loadJSON()

    def getAllValues(self):
        return self.jsonObject

    def getValue(self,key):
        return self.jsonObject[key]

    def setValue(self,key,value):
        self.jsonObject[key] = self._isInt(value)
        self._writeJSON()

    #check if value is int
    def _isInt(self,value):
        try:
            result = int(value)
            return result
        except:
            return value

    def _loadJSON(self):
	
        handle = open(self.jsonFile,'r')
        self.jsonObject = json.loads(handle.readline())
        handle.close()

    def _writeJSON(self):
        handle = open(self.jsonFile,'w')

        handle.write(json.dumps(self.jsonObject))
        handle.close()
