import sys, path
from math import sqrt
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
    def __init__(self,id:int, name:str, radius:int, team:int, alive:bool, position:tuple, concealed:bool, inCover:bool):
        self.id = id
        self.name = name
        self.radius = radius
        self.team = team
        self.alive = alive
        self.position = position
        self.concealed = concealed
        self.obsured = False
        self.inCover = inCover
        self.selected = False
        
        
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
        encoding.reverse()
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
            # print(modelEncoding.encoding)
            model = self.getModelByEncoding(modelEncoding.encoding)
            if model != None:
                teleportFlag = False
                for operative in self.operatives:
                    # Bandaid fix to prevent operatives teleporting to eachothers positions when mis-identified
                    # basically if an operative is already at the position of the model we are trying to move to
                    # we dont move the model
                    # This should prevent mis-identified operatives from stealing eachothers positions
                    if (self.getDistanceBetweenPoints(operative.position, modelEncoding.circleCenter) < 15):
                        teleportFlag = True
                        break
                if teleportFlag:
                    continue
                if self.getDistanceBetweenPoints(model.position, modelEncoding.circleCenter) > 15:
                    model.position = modelEncoding.circleCenter

    def setOperativeToObscured(self, id):
         for operative in self.operatives:
            if operative.id == id:
                operative.obsured = True
                
    def setOperativeToInCover(self, id):
        for operative in self.operatives:
            if operative.id == id:
                operative.inCover = True
                
    def resetOperativeSelection(self):
        for operative in self.operatives:
            operative.selected = False
            
    def getDistanceBetweenPoints(self, pointOne: tuple[int,int], pointTwo: tuple[int,int]):
        return sqrt((pointOne[0] - pointTwo[0])**2 + (pointOne[1] - pointTwo[1])**2)
    
    def removeOperative(self, id):
        for operative in self.operatives:
            if operative.id == id:
                self.operatives.remove(operative)
                break

    def swapOperativeState(self, id):
        for operative in self.operatives:
            if operative.id == id:
                operative.concealed = not operative.concealed
                break
      
    '''
    Use this function to define the operatives in use with their respective encodings
    '''
    def setupOperatives(self):
        # 0 through 15 are the pieces in use
        
        #Test with 5, 2, 13, 10
        # Team One
        self.addOperative(Operative(id = 5,name = "Five Team One",radius=42,team=1,alive=True,position=(400,200),concealed=True, inCover=False))
        # self.addEncoding(Operative(id = 2,name = "Two Team One",radius=14,team=1,alive=True,position=(300,300),obscured=False))
        # self.addOperative(Operative(id = 9,name = "Nine Team One",radius=42,team=1,alive=True,position=(300,300),concealed=False,inCover=False))
        # self.addOperative(Operative(id = 12,name = "Twelve Team One",radius=42,team=1,alive=True,position=(200,200),concealed=False,inCover=False))
        
        #Team Two
        # self.addOperative(Operative(id = 13,name = "Thirteen Team Two",radius=42,team=2,alive=True,position=(400,400),concealed=False,inCover=False))
        # self.addOperative(Operative(id = 10,name = "Ten Team Two",radius=42,team=2,alive=True,position=(500,500),concealed=False,inCover=False))
        self.addOperative(Operative(id = 3,name = "Three Team Two",radius=42,team=2,alive=True,position=(600,600),concealed=False,inCover=False))
        
        
    def scaleRadius(self, scale):
        for operative in self.operatives:
            operative.radius = operative.radius * scale

