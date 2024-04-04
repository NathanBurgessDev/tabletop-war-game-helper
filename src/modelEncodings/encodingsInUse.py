import sys, path
# from pygame import color

direction = path.Path(__file__).abspath()
sys.path.append(direction.parent.parent)
from markerIdentfication.combined import ModelEncoding

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)


# This stores a list of the encodings we are currently using

class Operative:
    def __init__(self,id:int, name:str, radius:int, team:int, alive:bool, position:tuple, obscured:bool):
        self.id = id
        self.name = name
        self.radius = radius
        self.team = team
        self.alive = alive
        self.position = position
        self.obsured = obscured
        
    def getColourRGB(self):
        if (self.team == 1):
            return RED
        elif (self.team == 2): 
            return BLUE

class OperativeList:
    def __init__(self):
        # ENCODINGS ARE LEFT TO RIGHT i.e. 1,2,1,2 = 10 (denary)
        self.encodings = []
        self.setupOperatives()
        
    # Add an encoding to the list
    def addEncoding(self, encoding: Operative):
        self.encodings.append(encoding)
    
    # Model ID is the ID of the model in base 10
    # Encodings are in base 2 (binary)
    # This acts as a helper function to get the model by its encoding
    def getModelByEncoding(self, encoding: list[int]) -> Operative | None:
        id = self.convertEncodingToId(encoding)
        for encoding in self.encodings:
            if encoding.id == id:
                return encoding
        return None
    
    # Converts a binary encoding to a base 10 number
    def convertEncodingToId(self, encoding: list[int]) -> int:
        finalEncoding = 0
        currentBitSize = 0
        for bit in encoding:
            if bit == 2:
                finalEncoding += 2**currentBitSize
            currentBitSize +=1
        return finalEncoding
    
    # We want to be able to update the positions of models in the encoding list
    def updateEncodingListPositions(self, modelEncodingList: list[ModelEncoding]):
        for modelEncoding in modelEncodingList:
            model = self.getModelByEncoding(modelEncoding.encoding)
            if model != None:
                model.position = modelEncoding.circleCenter

      

    def setupOperatives(self):
        # 0 through 15 are the pieces in use
        
        #Test with 5, 2, 13, 10
        # Team One
        self.addEncoding(Operative(id = 5,name = "Five Team One",radius=14,team=1,alive=True,position=(200,200),obscured=False))
        # self.addEncoding(Operative(id = 2,name = "Two Team One",radius=14,team=1,alive=True,position=(300,300),obscured=False))
        
        #Team Two
        # self.addEncoding(Operative(id = 13,name = "Thirteen Team Two",radius=14,team=2,alive=True,position=(400,400),obscured=False))
        self.addEncoding(Operative(id = 10,name = "Ten Team Two",radius=14,team=2,alive=True,position=(500,500),obscured=False))

