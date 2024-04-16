import sys, path
# from pygame import color

direction = path.Path(__file__).abspath()
sys.path.append(direction.parent.parent)
from markerIdentfication.combined import ModelEncoding

BOARD_SCALE = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)


# This stores a list of the encodings we are currently using

class Operative:
    def __init__(self,id:int, name:str, radius:int, team:int, alive:bool, position:tuple, obscured:bool, inCover:bool):
        self.id = id
        self.name = name
        self.radius = radius
        self.team = team
        self.alive = alive
        self.position = position
        self.obsured = obscured
        self.inCover = inCover
        
    def getColourRGB(self):
        if (self.team == 1):
            return RED
        elif (self.team == 2): 
            return BLUE

class OperativeList:
    def __init__(self):
        # ENCODINGS ARE LEFT TO RIGHT i.e. 1,2,1,2 = 10 (denary)
        self.operatives = []
        self.setupOperatives()
        
    # Add an encoding to the list
    def addOperative(self, operative: Operative):
        self.operatives.append(operative)
    
    # Model ID is the ID of the model in base 10
    # Encodings are in base 2 (binary)
    # This acts as a helper function to get the model by its encoding
    def getModelByEncoding(self, encoding: list[int]) -> Operative | None:
        id = self.convertEncodingToId(encoding)
        for operative in self.operatives:
            if operative.id == id:
                return operative
        return None
    
    def getModelById(self,id) -> Operative | None:
        for operative in self.operatives:
            if operative.id == id:
                return operative
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

    def setOperativeToObscured(self, id):
         for operative in self.operatives:
            if operative.id == id:
                operative.obsured = True
                
    def setOperativeToInCover(self, id):
        for operative in self.operatives:
            if operative.id == id:
                operative.inCover = True
      
    # Somewhat annoyingly the radius is relative to the DISPLAYED board size
    # and the position is relative to the ACTUAL board size
    # This doesnt really cause too many issues as the radius is only used for drawing and we never actually utilise the real radius
    # But it is something to be aware of
    def setupOperatives(self):
        # 0 through 15 are the pieces in use
        
        #Test with 5, 2, 13, 10
        # Team One
        self.addOperative(Operative(id = 5,name = "Five Team One",radius=42,team=1,alive=True,position=(300,200),obscured=False, inCover=False))
        # self.addEncoding(Operative(id = 2,name = "Two Team One",radius=14,team=1,alive=True,position=(300,300),obscured=False))
        
        #Team Two
        # self.addEncoding(Operative(id = 13,name = "Thirteen Team Two",radius=14,team=2,alive=True,position=(400,400),obscured=False))
        self.addOperative(Operative(id = 10,name = "Ten Team Two",radius=42,team=2,alive=True,position=(500,800),obscured=False,inCover=False))
        
        
    def scaleRadius(self, scale):
        for operative in self.operatives:
            operative.radius = operative.radius * scale

