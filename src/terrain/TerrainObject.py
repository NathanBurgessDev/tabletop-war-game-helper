import pygame        
from shapely import Polygon
from shapely import affinity
# A terrain object is a collection of points that make up the terrain X
# Each point is a tuple of (x, y) coordinates
# Each point has a line between itself, then next point, and the previous point
# A minimum of 3 points is required to make a terrain object
class Terrain:
    verticies = []
    heavy = False
    id = None
    scaledPolygon = None
    def __init__(self, points: list[tuple[int,int]], heavy: bool = False, id: int = 0):
        if len(points) < 3:
            raise ValueError("Terrain object must have at least 3 points")
        self.id = id
        self.verticies = points
        self.heavy = heavy
        self.polygonLineSegments = self.getPolygonLineSegments()
        self.linePointMembers = self.pointLineSegmentMembers()
        
    def getPolygonLineSegments(self):
        lineSegments = []
        for i in range(0, len(self.verticies)):
            lineSegments.append((self.verticies[i], self.verticies[(i+1) % len(self.verticies)]))
        return lineSegments
    
    # For each point in the polygon we want to get the 2 lines it is a part of 
    def pointLineSegmentMembers(self):
        pointMembers = {}
        for i in range(0, len(self.verticies)):
            pointMembers[self.verticies[i]] = [self.verticies[i-1], self.verticies[(i+1) % len(self.verticies)]]
        return pointMembers
    
    def updateVerticies(self):
        self.verticies = list(self.scaledPolygon.exterior.coords[:-1])
        self.polygonLineSegments = self.getPolygonLineSegments()
        self.linePointMembers = self.pointLineSegmentMembers()
        
    def updatePolygon(self):
        polygon = Polygon(self.verticies)
        self.scaledPolygon = polygon
        self.polygonLineSegments = self.getPolygonLineSegments()
        self.linePointMembers = self.pointLineSegmentMembers()
        
    def translatePolygon(self, xoff, yoff):
        self.scaledPolygon = affinity.translate(self.scaledPolygon, xoff, yoff)
        self.updateVerticies()
        
    def rotatePolygon(self, angle):
        self.scaledPolygon = affinity.rotate(self.scaledPolygon, angle, origin = "centroid")
        self.updateVerticies()
        
    def scalePolygon(self, xfact, yfact):
        self.scaledPolygon = affinity.scale(self.scaledPolygon, xfact, yfact)
        self.updateVerticies()
        
  
    def findXandYTranslation(self,moveTo: tuple[int,int],current: tuple[int,int]):
        xTranslation = moveTo[0] - current[0]
        yTranslation = moveTo[1] - current[1]
        return (xTranslation,yTranslation) 
        
    
        
class TerrainLine:
    def __init__(self, start: tuple[int,int], end: tuple[int,int], heavy : bool ):
        self.start = start
        self.end = end
        self.heavy = heavy
        self.line = (start, end)
        
# 5.6mm Wall Width
# 78.81 Wall length
# 24.67 Pillar Width
# 28.95 pillar length

# 24.67 /2 = 12.335
#5.6 / 2 = 2.8
# 12.335 - 2.8 = 9.535
# 12.335 + 2.7 = 15.135
class PillarDoubleWall(Terrain):
    def __init__(self, id):
        super().__init__(points=self.buildPolygon(), heavy = True, id = id)
    
    # I built this upside down :((((((((((((((((((((((((((((((((((((((((((((((
    def buildPolygon(self):
            verts = [(100,100), (109.5,100),(109.5, 178.8),(115.1,178.8), (115.1,100),(124.6,100),(124.6,71.05),(115.1,71.05), (115.1,-7.76), (109.5,-7.76), (109.5,71.05), (100,71.05)]
            polygon = Polygon(verts)
            # self.scaledPolygon = affinity.scale(polygon, xfact=3, yfact = 3)
            self.scaledPolygon = polygon
            scaledVerts = list(self.scaledPolygon.exterior.coords[:-1])
            print(scaledVerts)
            return scaledVerts
    
        