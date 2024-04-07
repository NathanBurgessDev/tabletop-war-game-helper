import pygame        
# A terrain object is a collection of rectangles that make up the terrain X
# A terrain object is a collection of polygons 
class Terrain:
    terrainRectangles = []
    def __init__(self):
        pass
    def addRectangle(self,width,height, topLeftX, topLeftY):
        self.terrainRectangles.append(pygame.Rect(topLeftX,topLeftY,width,height))
    
    