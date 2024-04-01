# This stores a list of the encodings we are currently using

class Operative:
    def __init__(self,id:int, name:str, radius:int, team:int, alive:bool, position:tuple):
        self.id = id
        self.name = name
        self.radius = radius
        self.team = team
        self.alive = alive
        self.position = position

class OperativeList:
    def __init__(self):
        self.encodings = []
        
    def addEncoding(self, encoding: Operative):
        self.encodings.append(encoding)
        
    def getModelByEncoding(self, encoding: list[int]) -> Operative | None:
        id = self.convertEncodingToId(encoding)
        
        for encoding in self.encodings:
            if encoding.id == id:
                return encoding
        return None
    
    def convertEncodingToId(self, encoding: list[int]) -> int:
        encoding = 0
        currentBitSize = 0
        for bit in encoding:
            if bit == 2:
                encoding += 2**currentBitSize
            currentBitSize +=1
        return encoding
    
    
    # We want to be able to update the positions of models in the encoding list
    def updateEncodingListPositions():
        pass
        

def setupOperatives() -> OperativeList:
    # 0 through 15 are the pieces in use
    
    #Test with 5, 2, 13, 10
    encodingList = OperativeList()
    
    # Team One
    encodingList.addEncoding(Operative(id = 5,name = "Five Team One",radius=14,team=1,alive=True,position=(0,0)))
    encodingList.addEncoding(Operative(id = 2,name = "Two Team One",radius=14,team=1,alive=True,position=(0,0)))
    
    #Team Two
    encodingList.addEncoding(Operative(id = 13,name = "Thirteen Team Two",radius=14,team=2,alive=True,position=(0,0)))
    encodingList.addEncoding(Operative(id = 10,name = "Ten Team Two",radius=14,team=2,alive=True,position=(0,0)))

    return encodingList