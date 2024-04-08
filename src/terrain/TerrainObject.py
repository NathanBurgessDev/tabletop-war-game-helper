import pygame        
# A terrain object is a collection of points that make up the terrain X
# Each point is a tuple of (x, y) coordinates
# Each point has a line between itself, then next point, and the previous point
# A minimum of 3 points is required to make a terrain object
class Terrain:
    verticies = []
    def __init__(self, points: list[tuple[int,int]]):
        if len(points) < 3:
            raise ValueError("Terrain object must have at least 3 points")
        self.verticies = points
        
    def getPolygonLineSegments(self):
        lineSegments = []
        for i in range(0, len(self.verticies)):
            lineSegments.append((self.verticies[i], self.verticies[(i+1) % len(self.verticies)]))
        return lineSegments
    
    