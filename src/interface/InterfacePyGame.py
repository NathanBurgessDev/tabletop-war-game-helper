import pygame
import numpy as np
import sys
import cv2 as cv
from math import sqrt
# from pathlib import Path
import path
# path_root = Path(__file__).parents[2]
# print(path_root)
# sys.path.append('../')
direction = path.Path(__file__).abspath()
sys.path.append(direction.parent.parent)
from markerIdentfication.combined import ModelFinder
from modelEncodings.encodingsInUse import Operative, OperativeList
from terrain.TerrainObject import Terrain, TerrainLine

# Initialize Pygame
pygame.init()

# Scaling
SCREEN_SCALE = 4
BOARD_SCALE = 3

# Screen dimensions
SCREEN_WIDTH = 559 * SCREEN_SCALE
SCREEN_HEIGHT = 381 * SCREEN_SCALE

# Game board dimensions
BOARD_WIDTH = 559 * BOARD_SCALE # 1677 - 22 inches
BOARD_HEIGHT = 381 * BOARD_SCALE # 1143 - 15 inches

BOARD_INCH = round(25.4 * BOARD_SCALE)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

# Circle radius
# Spent a while being confused - found out I was using radius not diameter
CIRCLE_RADIUS = 14 * BOARD_SCALE

class BarycentricCoordinates:
    def __init__(self,alpha,beta,gamma):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

class GameBoard:
    gameBoardRect = pygame.Rect((SCREEN_WIDTH - BOARD_WIDTH) // 2, 50, BOARD_WIDTH, BOARD_HEIGHT)
    imageInch = None
    terrainList = []
    def __init__(self,screen,imageSize = (0,0)):
        if (imageSize == (0,0)):
            self.setTestMode()
            self.screen = screen
        else:
            self.imageSize = imageSize
            self.screen = screen
        
    def drawOperative(self, operative: Operative):

        pygame.draw.circle(self.screen, operative.getColourRGB(), operative.position, operative.radius)
        
      
        # print("Operative Point")
        # print(self.translatePointToBoardSize(operative.position))
        # Draw the name of the operative
        font = pygame.font.Font(None, 36)
        text = font.render(operative.name, True, WHITE)
        self.screen.blit(text, operative.position)
        
    def drawOperativeObscured(self, operative: Operative):
        pygame.draw.circle(self.screen, YELLOW, operative.position, operative.radius)
        
        # Draw the name of the operative
        font = pygame.font.Font(None, 36)
        text = font.render(operative.name, True, WHITE)
        self.screen.blit(text, operative.position)
        
    def drawCircle(self, circle: tuple[int,int], radius: int):
        pygame.draw.circle(self.screen, MAGENTA, circle, radius)
        

        # print("Points")
        # print(self.translatePointToBoardSize(circle))
        
    def drawLine(self, start: tuple[int,int], end: tuple[int,int]):
        pygame.draw.line(self.screen, MAGENTA,start, end)
        
    def addTerrain(self, terrain: Terrain):
        self.terrainList.append(terrain)
        
    def getBoardToImageWidthScale(self):
        return BOARD_WIDTH / self.imageSize[1]
    
    def getBoardToImageHeightScale(self):
        return BOARD_HEIGHT / self.imageSize[0]
    
    def getImageToBoardWidthScale(self):
        return self.imageSize[1] / BOARD_WIDTH
        
    def getImageToBoardHeightScale(self):
        return self.imageSize[0] / BOARD_HEIGHT
    # This took a while to get working
    # We need to translate the circle center from the size of the image to the size of the baord
    # To do this we need to use a scale factor to translate the circle center and then move it to be relative to the 0,0 of the board display
    # As opposed to the 0,0 of the screen
    # Spent a while on this cause imageSize is in the format (height, width) and I was using it as (width, height)
    def translatePointToBoardSize(self, point: tuple[int,int]) -> tuple[int,int]:
        newX = (point[0] * (self.getBoardToImageWidthScale())) + ((SCREEN_WIDTH - BOARD_WIDTH) // 2)
        newY = (point[1] * (self.getBoardToImageHeightScale())) + 50
        return (int(newX), int(newY))
    
    def setTestMode(self):
        self.imageSize = (BOARD_HEIGHT,BOARD_WIDTH)
        
    def drawGameBoard(self):
        pygame.draw.rect(self.screen, BLACK, self.gameBoardRect)
        # Center of the game board
        pygame.draw.circle(self.screen, BLUE,(((SCREEN_WIDTH - BOARD_WIDTH) // 2) + (BOARD_WIDTH // 2),(BOARD_HEIGHT // 2) + 50), 10)
        
    def drawTerrain(self):
        for terrain in self.terrainList:
            pygame.draw.polygon(self.screen, ORANGE, terrain.verticies,0)
        
                
            




class MainGame:
    def __init__(self, operativeList: OperativeList, testing: bool):
        self.operativeList = operativeList
        self.testingFlag = testing
        self.setupScreen()
        if (testing):
            self.setupModelFinderTesting()
            self.setupGameBoardTesting()
        else:
            imageSize = self.setupModelFinder()
            self.setupGameBoard(imageSize)
        self.gameLoop()
        
    def setupModelFinder(self):
        filePath = "testImages/paperTestCorners.jpg"
        
        image = cv.imread(filePath)
        image = cv.rotate(image, cv.ROTATE_90_CLOCKWISE)
        
        self.modelFinder = ModelFinder(image)
        gameBoardData = self.modelFinder.identifyModels(image, self.modelFinder.cornerPoints)
        return gameBoardData[1]
        
    def setupModelFinderTesting(self):
        pass
            
    
    def setupScreen(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game Board")
        
    def setupGameBoard(self, imageSize):
        self.gameBoard = GameBoard(screen=self.screen,imageSize=imageSize)
        
    def setupGameBoardTesting(self):
        self.gameBoard = GameBoard(screen=self.screen)
        
        
    def gameLoop(self):
        # print("game loop")
        # print(self.gameBoard.getBoardToImageHeightScale())
        # print(self.gameBoard.getBoardToImageWidthScale())
        
        
        
        # Testing purposes we do an inital update
        if (not self.testingFlag):
        
            filePath = "testImages/paperTestCorners.jpg"
            
            image = cv.imread(filePath)
            image = cv.rotate(image, cv.ROTATE_90_CLOCKWISE)
            
            gameBoardData = self.modelFinder.identifyModels(image,self.modelFinder.cornerPoints)
            self.gameBoard.imageSize = gameBoardData[1]
            
            if (gameBoardData[0] != None):
                operativeList.updateEncodingListPositions(gameBoardData[0])
            
                
        if (self.testingFlag):
            terrainVertecies = [(300,500),(300,550),(400,550),(400,500)]
            for vertex in terrainVertecies:
                terrainVertecies[terrainVertecies.index(vertex)] = self.gameBoard.translatePointToBoardSize(vertex)
            terrain = Terrain(terrainVertecies, heavy=True)
            # terrain.addRectangle(self.gameBoard.imageInch ,self.gameBoard.imageInch/2 ,300,350)
            self.gameBoard.addTerrain(terrain)
            
        # Transform the operatives to be within the board scale
        for operative in self.operativeList.operatives:
            operative.position = self.gameBoard.translatePointToBoardSize(operative.position)
            
        #Transform the terrain to be within the board scale
        # for terrain in self.gameBoard.terrainList:
        #     for i in range(0,len(terrain.verticies)):
        #         terrain.verticies[i] = self.gameBoard.translatePointToBoardSize(terrain.verticies[i])
        
        
        while True:
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            for operative in self.operativeList.operatives:
                operative.obsured = False

            # Clear the screen
            self.screen.fill(GRAY)

            # Draw the game board
            self.gameBoard.drawGameBoard()
            
            #Draw terrain
            self.gameBoard.drawTerrain()
            
           
            self.checkLineOfSight(10)
            
                

            # Draw operatives on the game board        
            for operative in self.operativeList.operatives:
                if (operative.obsured):
                    self.gameBoard.drawOperativeObscured(operative)
                else:
                    self.gameBoard.drawOperative(operative)
                    
            
            

            # Update the display
            pygame.display.flip()
            
    
   
       
                
    def checkLineOfSight(self, operativeID):
        chosenOperative = self.operativeList.getModelById(operativeID)
     
        for operative in self.operativeList.operatives:
            if (chosenOperative.team != operative.team):
                # Draw 2 Firing cones from the extreme of each circle to the extremes of the other circle
                # Get the gradient of the line between the two circles
                # Take the negative of the gradient to get the perpendicular gradient
                # For each circle
                # Get the intercepts of the perpendicular lines with the circle
                # Draw a triangle between these three points
                
                
                chosenOperativePoints = self.getCircleExtremes(chosenOperative.position[0],chosenOperative.position[1],chosenOperative.radius,operative.position[0],operative.position[1])
                
                targetOperativePoints = self.getCircleExtremes(operative.position[0],operative.position[1],operative.radius,chosenOperative.position[0],chosenOperative.position[1])
                
                # print("Operative Radius")
                # print(operative.radius)
                

                
       
                # self.gameBoard.drawCircle(chosenOperativePoints[0],5)
                # self.gameBoard.drawCircle(chosenOperativePoints[1],5)
                
                
                # self.gameBoard.drawCircle(targetOperativePoints[0],5)
                # self.gameBoard.drawCircle(targetOperativePoints[1],5)
                
       
                
                plusTriangle = [chosenOperativePoints[0],targetOperativePoints[1],targetOperativePoints[0]]
                
                
                
                self.gameBoard.drawLine(plusTriangle[0],plusTriangle[1])
                self.gameBoard.drawLine(plusTriangle[1],plusTriangle[2])
                self.gameBoard.drawLine(plusTriangle[2],plusTriangle[0])
                
                
                minusTriangle = [chosenOperativePoints[1],targetOperativePoints[0],targetOperativePoints[1]]
                
                self.gameBoard.drawLine(minusTriangle[0],minusTriangle[1])
                self.gameBoard.drawLine(minusTriangle[1],minusTriangle[2])
                self.gameBoard.drawLine(minusTriangle[2],minusTriangle[0])
                
                
                terrainLinesPositive = self.getLinesInFiringCone(plusTriangle)
                terrainLinesNegative = self.getLinesInFiringCone(minusTriangle)
                
                # For each object
                # Check if any of the points are within the firing cone
                
                if (self.isObscured(chosenOperative,operative,terrainLinesPositive) and self.isObscured(chosenOperative,operative,terrainLinesNegative)):
                    self.operativeList.setOperativeToObscured(operative.id)
                
                if (self.isInCover(chosenOperative,operative,terrainLinesPositive) and self.isInCover(chosenOperative,operative,terrainLinesNegative)):
                    self.operativeList.setOperativeToObscured(operative.id)
                
                        
                            
    # We want to check 2 things
    # If a line of terrain intersects the firing cone
    # If a point of terrain is within the firing cone
    
    # We want to do the lines first as it is easier to assume the terrain is entirely within the firing cone
    # Which would be the case if there are no intersectionsw
    
    # If a point is within the firing line we then need to find the closest point on the line segment to the center of the circle
    # To do this we take the 2 lines the point is a part of and find the closest point on the line to the center of the circle

    
    # Alternatively we could think of this as "find the closest point in the object, that is inside the firing cone, to the center of the circle - "
    # To do this we need to take each line - and clip it to be within the firing cone
    # Then find the closest point on the line to the center of the circle
    # Repeat until we have one that satisfies Obscurity or we run out of terrain
    
    # As objects are not filled we can think of the object as a collection of lines defined by the verticies
    
    # Find the points of the line within the firing cone
    # Take a line -> check if the start or end is within the triangle
    # If they are use the start and end points
    # If One is and one isnt - take the point that is within the triangle and find the intersect of the line with the firing cone
    # If neither are - find the 2 points that intersect the firing cone
    # If there are no intercepts - that line is not in the firing cone
    
    # If we have 2 points that are within the firing cone - find the closest point on the line to the center of the circle
    # Check if that distance - circle radius is > 2 inches    
    
    
    
    # This technically doesnt cover other operatives counting as cover - but we will leave that out for now 
    
    # Checks for 2 things to be in cover
    # Defender must be more than 2 inches from the Attacker
    # Defender must be within 1 inch of a piece of terrain that covers a cover line
    def isInCover(self, attacker: Operative, defender: Operative, terrain: list[TerrainLine]) -> bool:
        
        distanceFromAttackerToDefender = self.getDistanceBetweenPoints(attacker.position,defender.position)
            
        if (distanceFromAttackerToDefender < BOARD_INCH*2):
            return False
        
        for lineSegment in terrain:
            closestPointDefender = self.getClosestPointOnLineSegment(lineSegment.line,defender.position)

            # Check if the distance between the closest point and the center of the circle is less than 2 inches
            # Since we are working within world space (board space) the sizes are known,

            distanceToDefender = self.getDistanceBetweenPoints(closestPointDefender,defender.position)
            distanceToDefender = distanceToDefender - defender.radius

            if (distanceToDefender <= BOARD_INCH):
                return True
            
        return False
    
                                              
    def isObscured(self, attacker: Operative, defender: Operative, terrain: list[TerrainLine]):
        for lineSegment in terrain:
            if (lineSegment.heavy):
                # Get the closest point on the line to the center of the circle of the target operative
                closestPointDefender = self.getClosestPointOnLineSegment(lineSegment.line,defender.position)

                # Check if the distance between the closest point and the center of the circle is less than 2 inches
                # Since we are working within world space (board space) the sizes are known,

                distanceToDefender = self.getDistanceBetweenPoints(closestPointDefender,defender.position)
                distanceToDefender = distanceToDefender - defender.radius

                distanceToShooter = self.getDistanceBetweenPoints(closestPointDefender,attacker.position)
                distanceToShooter = distanceToShooter - attacker.radius



                closestPointAttacker = self.getClosestPointOnLineSegment(lineSegment.line,attacker.position)

                distanceToDefender1 = self.getDistanceBetweenPoints(closestPointAttacker,defender.position)
                distanceToDefender1 = distanceToDefender1 - defender.radius

                distanceToShooter1 = self.getDistanceBetweenPoints(closestPointAttacker,attacker.position)
                distanceToShooter1 = distanceToShooter1 - attacker.radius


                # print(f"Distance to Defend",distanceToDefender)
                # print(f"2 Inches",BOARD_INCH*2)
                if (distanceToDefender >= BOARD_INCH*2 and distanceToShooter >= BOARD_INCH):
                    # print(f"distanceToDefender: ",distanceToDefender / BOARD_INCH)
                    # print(f"distanceToShooter: ",distanceToShooter / BOARD_INCH)
                    self.gameBoard.drawCircle(closestPointDefender,5)

                    # self.gameBoard.drawLine(newLine[0],newLine[1])
                    return True
                if (distanceToDefender1 >= BOARD_INCH*2 and distanceToShooter1 >= BOARD_INCH):
                    # print(f"distanceToDefender: ",distanceToDefender / BOARD_INCH)
                    # print(f"distanceToShooter: ",distanceToShooter / BOARD_INCH)
                    self.gameBoard.drawCircle(closestPointAttacker,5)
                    
                    # self.gameBoard.drawLine(newLine[0],newLine[1])
                    return True
        return False
                      
                      
                      
    def getLinesInFiringCone(self, triangle: list[tuple[int,int]]) -> list[TerrainLine] | None:
        newTerrainLineList = []
        for terrain in self.gameBoard.terrainList:
            for lineSegment in terrain.polygonLineSegments:
                newLine = self.constructNewLine(lineSegment,triangle)
                if (newLine != None):
                    newTerrainLineList.append(TerrainLine(newLine[0],newLine[1],terrain.heavy))
        
        return newTerrainLineList
                      
    # This would make sense to de recursively  
    def constructNewLine(self, lineSegment: tuple[tuple[int,int],tuple[int,int]], triangle) -> tuple[tuple[int,int],tuple[int,int]] | None:
        # Check if point is within the triangle
        newLine = []
        if (self.isPointInTriangle(lineSegment[0],triangle)):
            newLine.append(lineSegment[0])
        if (self.isPointInTriangle(lineSegment[1],triangle)):
            newLine.append(lineSegment[1])
        
        # If both points are within the triangle
        if (len(newLine) == 2):
            return (newLine[0],newLine[1])
        
        lineTriangleIntercept = self.getLineTriangleIntercept(lineSegment,triangle)
        # self.gameBoard.drawCircle(lineSegment[0],5)
        # self.gameBoard.drawCircle(lineSegment[1],5)
        if (lineTriangleIntercept != None):
            for line in lineTriangleIntercept:
                if (newLine == []):
                    newLine.append(line)
                elif newLine[0] != line:
                    newLine.append(line)
            
        if len(newLine) != 2:
            return None
        
        if (newLine[0] == newLine[1]):
            return None
        
        return (newLine[0],newLine[1])
        
        # print(lineTriangleIntercept)
             
   
    
    def getLineTriangleIntercept(self, line: tuple[tuple[int,int],tuple[int,int]], triangle: list[tuple[int,int]]) -> tuple[tuple[int,int],tuple[int,int] | None | tuple[int,int]]:
        A = (triangle[0],triangle[1])
        B = (triangle[1],triangle[2])
        C = (triangle[2],triangle[0])
        
        aLineIntercept = self.getLineLineIntercept(line,A)
        bLineIntercept = self.getLineLineIntercept(line,B)
        cLineIntercept = self.getLineLineIntercept(line,C)
        
        intercepts = []
        
        if (aLineIntercept != None):
            intercepts.append(aLineIntercept)
        if (bLineIntercept != None):
            intercepts.append(bLineIntercept)
        if (cLineIntercept != None):
            intercepts.append(cLineIntercept)
            
        return intercepts
       
    
    # https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
    def getLineLineIntercept(self, lineOne: tuple[tuple[int,int],tuple[int,int]], lineTwo: tuple[tuple[int,int],tuple[int,int]]) -> tuple[int,int] | None:
        
        a = np.array(lineOne[0])
        b = np.array(lineOne[1])
        c = np.array(lineTwo[0])
        d = np.array(lineTwo[1])
      
        
        h1 = self.computeH(a,b,c,d)
        h2 = self.computeH(c,d,a,b)
        
        if (h1 == None or h2 == None):
            return None
        
        if (h1 > 0 and h1 < 1 and h2 > 0 and h2 < 1):
            tupleIntercept= tuple(c + h1 * (d - c))
            
            returnTuple = (int(tupleIntercept[0]),int(tupleIntercept[1]))
            return returnTuple
        
        
        return None
            
    # https://jsfiddle.net/ferrybig/eokwL9mp/
    def computeH(self, a,b,c,d):
        e = b - a
        f = d - c
        p = np.array([-e[1],e[0]])
        # The lines are parrallel
        if (f.dot(p) == 0):
            return None
        h = ((a-c).dot(p)) / (f.dot(p))
        return h
  
    # https://stackoverflow.com/questions/47177493/python-point-on-a-line-closest-to-third-point
    # DEPRECATED
    def getClosestPointOnLine(self, line: tuple[tuple[int,int],tuple[int,int]], point: tuple[int,int]):
        
        x1, y1 = line[0]
        x2, y2 = line[1]
        x3, y3 = point
        
        dx, dy = x2 - x1, y2 - y1
        det = dx * dx + dy * dy
        a = (dy * (y3 - y1) + dx * (x3 - x1)) / det
        return (int(x1 + a * dx), int(y1 + a * dy))
    
      # https://gdbooks.gitbooks.io/3dcollisions/content/Chapter1/closest_point_on_line.html
    def getClosestPointOnLineSegment(self, line: tuple[tuple[int,int],tuple[int,int]], point: tuple[int,int]):
        # Break ab apart into components a and b
        a = line[0]
        b = line[1]

        # Project c onto ab, computing the parameterized position d(t) = a + t * (b - a)
        t = self.dotProduct((point[0] - a[0], point[1] - a[1]), (b[0] - a[0], b[1] - a[1])) / self.dotProduct((b[0] - a[0], b[1] - a[1]),(b[0] - a[0], b[1] - a[1]))

        # Clamp T to a 0-1 range. If t was < 0 or > 1 then the closest point was outside the line!
        t = self.clamp(t, 0, 1)

        # Compute the projected position from the clamped t
        d = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))

        # Return result
        return d
    
    def dotProduct(self, a: tuple[int,int], b: tuple[int,int]):
        return a[0] * b[0] + a[1] * b[1]
        
    def clamp(self,value, min_val, max_val):
        return max(min_val, min(value, max_val))
        
    def getDistanceBetweenPoints(self, pointOne: tuple[int,int], pointTwo: tuple[int,int]):
        return sqrt((pointOne[0] - pointTwo[0])**2 + (pointOne[1] - pointTwo[1])**2)
        
        
        
        
        
                
    # Best to use barycentric coordinates for this          
    def isPointInTriangle(self, point, triangle):
        barycentricCoordinates = self.getBarycentricCoordinates(point,triangle)
        
        if ((barycentricCoordinates.alpha >= 0 and barycentricCoordinates.alpha <= 1)and (barycentricCoordinates.beta >= 0 and barycentricCoordinates.beta <=1) and (barycentricCoordinates.gamma >= 0 and barycentricCoordinates.gamma <= 1)):
            return True
        return False
        
    
    def getBarycentricCoordinates(self, point: tuple[int,int], triangle: list[tuple[int,int]]) -> BarycentricCoordinates:
        A = triangle[0]
        B = triangle[1]
        C = triangle[2]
        
        lineBCP = self.getImplicitLineEquation(B,C,point)
        lineBCA = self.getImplicitLineEquation(B,C,A)
        
        alpha = lineBCP / lineBCA
        
        lineACP = self.getImplicitLineEquation(A,C,point)
        lineACB = self.getImplicitLineEquation(A,C,B)
        
        beta = lineACP / lineACB
        
        lineABP = self.getImplicitLineEquation(A,B,point)
        lineABC = self.getImplicitLineEquation(A,B,C)
        
        gamma = lineABP / lineABC
        
        # Mildly fedup of just returning a tuple
        # struct would be nicer but python has forced my hand
        return BarycentricCoordinates(alpha,beta,gamma)
        
        
        
        
        
    def getImplicitLineEquation(self, A,B,P):
        line = (B[1] - A[1]) * P[0] + (A[0] - B[0]) * P[1] + B[0] * A[1] - A[0] * B[1]
        return line
        
    
    def getCircleExtremes(self, h,k,r, targetX, targetY) -> tuple[tuple[int,int],tuple[int,int]]:
        
        
        
        
        # Problem
        # When the gradient is < 0.01 we lose precision
        # As the gradient gets smaller when we calcualte the reciprocal we lose everything after the first decimal place
        # As a result the further we go down our calculations the error increases
        
        # i.e for a gradient of 0.0333333333 we get a reciprocal of -30.0
        
        # This issue was actually caused by the rounding on finalXplus etc etc
        
        
        # Another problem
        # If the gradient is 0 we can't get the reciprocal (this is the case when the targets are the same y value)
        # We need to handle this case
        # If the gradient is 0 then the line intersects are the top and bottom of the circle
        # We already know the x and y of the circle
        # and the radius
        # So we can just add and subtract the radius from the y value
        
        # Another problem
        # Targets are on the same x value
        # We can't get the gradient as its / 0 
        
        if (targetX == h):
            finalXplus = h + r 
            finalXminus = h - r
            finalYplus = k 
            finalYminus = k 
            return ((finalXminus,finalYminus),(finalXplus,finalYplus))
        
        gradient = (k- round(targetY)) / (h - round(targetX))
        if (gradient != 0):
            positivePerpendicularGradient = np.reciprocal(gradient)
            perpendicularGradient = np.negative(positivePerpendicularGradient)
            c = k - (perpendicularGradient * (h))
            m = perpendicularGradient
            
            finalXplus = (h-m*c+m*k + sqrt(-(m**2 * h**2)+ 2 *(m*k*h)-2*(m*c*h)+ (m**2 * r**2) + 2*(c*k) + r ** 2 - c**2 - k**2))/(1+m**2)
                    
            finalXminus = (h-m*c+m*k - sqrt(-(m**2 * h**2)+ 2 *(m*k*h)-2*(m*c*h)+ (m**2 * r**2) + 2*(c*k) + r ** 2 - c**2 - k**2))/(1+m**2)
            
            finalYplus = (m * finalXplus + c)
            
            finalYminus = (m * finalXminus + c)
        else:
            finalXplus = h
            finalXminus = h
            finalYplus = k + r
            finalYminus = k - r
        
       
       
        # self.gameBoard.drawLine((0,c),(h,k))
        # self.gameBoard.drawLine((h,k),(targetX,targetY))
        
       
        
 
        
        # self.gameBoard.drawCircle((finalXplus,finalYplus),5)
        # self.gameBoard.drawCircle((finalXminus,finalYminus),5)
        
        
        # print(finalXminus,finalYminus)
        # print(finalXplus,finalYplus)
                
        
        return ((finalXminus,finalYminus),(finalXplus,finalYplus))
            
   
        
        
        

if __name__ == "__main__":
    operativeList = OperativeList()
    game = MainGame(operativeList,True)


# 30/03/24
# Circle to display in correct position is now complete
# Issues today - I was using the wrong dimensions for the image size
# I was using (height, width) instead of (width, height)
# Translating to thte correct place on the board was a bit of a pain - need to get a scale factor and then change where 
# WE considered the origin to be 
# Python relative file paths were annoying to do
# Added homogrophy to have the user select the 4 corners of the board on startup - this will be used to transform the image
# To be flat on the screen, define the size of the board, and allow us to treat the image as if it was hte full board - makes translation much easier to do
# In the future this corner selection *should* be automated using AR tags / QR codes / coloured corners 

# Things to improve on
# Drawing based on encoding, placing the ID / name of model on the circle
# Click to select
# Right click to select other team's piece
# Drawing based on team
# GetCircleData should simply update a current dictionary of circles in use
# So when a circle can't be found we still display the last known position.


# 01/04/24
# Restructured the repository to be cleaner and more readable
# Struggled with python file paths - had to use the absolute path - required some re-sturcturing and time
# Added a new class Operative to store the data of the models
# Added a new class OperativeList to store a list of Operative objects
# Made it convert the encodings to a readable ID
# Still need to work on updating the list and displaying it with the new data
# TODO - Write about the circles sizes, if the circle is too big it will mis-edentify and be wierd
# Also write about circle detection sometimes getting hte inside of the circle and not the outside and how this causes problems with getting radius
# Woke up at like 5pm today - BST is not fun

# Once we are drawing the circles based on the encoding we need to do a few main things:
# 1. Get Video Feed working
# 2. Get selection of operatives working
# 2.1 storing the game state in a 2D array to show operative positions and terrain - probably do not need to do this
# 3. Get movement of operatives working
# 4. Next turn button
# 5. Get RayCasting working (primative terrain)  - Prioritising this as it is quite complicated
# 6. Terrain


# 02/04/24
# Droidcam / Irun webcam
# If I want to use a proper camera I need a capture card
# Droidcam may only be SD output not HD
# Irun is only for ubuntu 
# Droidcam: v4l2loopback-dc fails to compile on kernels 6.8+
# Patched 2 weeks ago - supposobly merged to main branch but doesnt seem to be working
# Continunity Camera
# Logitech webcam now works with good framerate - however only 1080p :(
# sudo modprobe v4l2loopback fixed the problem - kernal update
# Getting 1920x1080 input from webcam is very very slow - this is an openCV problem, works fine in OBS or Kamoso
# Getting webcam input can be difficult - /dev/video?
# Where ? is the number of the camera, we would pass /dev/video0 for the default camera
# for some reason video1 always fails and video2 is our "other" camera
# droidcam will take over video2 though webcam can sometimes take over video0

# Spent some time refactoring the code to let calibration be more easily done, storing the corner points in an object so we can use them for each image (part of getting video working)
# Made the program much more OOP - GameBoard, Operative, OperativeList, and soon to be GameState
# We call an initial calibration on startup to get the corner points of the board
# After this we store the corner points in the GameBoard object and use them to translate the video feed
# Next steps are to get the video feed working and then to get the selection of operatives working
# Now in the loop we draw a list of the operative on the board in OperativeList
# We update OperativeList with the operatives we found in the image
# This way if we miss a circle we can still display the last known position

# From here we need to get the video feed working 
# selection of operatives
# store the game state in a 2D array i.e - size of game board, each position is a number representing the space the operative is taking up, 255 for empty and 254 for terrain (Should probably use some enums)
# Added some error checking to the circle detection
# If we find an encoding we're not using, we dont have anything to update - helps reduce false positives


# 03/04/24
# So kill team cover rules are a pain
# Question 1 - Can attackers head see any part of the defender - Center of model to any part of the defender
# Question 2 - Concealment or engaged
# Q3 - if engaged Visable + not obscured
# Q4 - if concealed - Visable + not obscured + not in cover 

# https://www.reddit.com/r/killteam/comments/vukgpz/basic_line_of_sight_rule_slate_i_made_for_our/
# Obscurity - good lord this one is not easy
# Fire cone - One point on the base - to EVERY point on a defender
# Similar to drawing a triangle from the base to the defender
# Could just check if I draw a rectangle between 2 pieces if that rectangle covers any terrain
# If no - No cover
# If yes - There is some cover, still need to find out how much
# Right, left, top, bottom of attacker circle. Draw a triangle (?)
# Get intersects
# Check range of intersects - if defender >2" from intersect -> obscured
# If <=1" -> that part of the terrain is not obscuring the defender

# Determine Cover 
# >2" away -> are they <1" from Terrain  -> in cover 

# What if center of cricle ends up outside of bounds???

# 04/04/24
# We're gonna model this as "simple" terrain i.e. just simple rectangles
# If we wanted to do more complex terrain we would likely need to use a more complex approach
# Either making a 2D representation of the game board and then performing raycasting from there
# Or using barycentric coordinates to calculate whether objects fall within the firing cone.
# This approach would be useful but would be incredibly slow without multithreading / GPU
# As it is every pixel in the firing cone for every peice of terrain / model.
# repeated for each possible firing cone from the model
# For now we will simly check collisions within a firing cone within the area of our simple terrain objects

# All game logic is performed on the original coordinates (from the image) which are then translated to the game board abstraction when drawing


# 05/04/24
# FIRING CONE YIPEEE
# Was a massive pain to get working 
# I cant do maths (gcse level)
# TLDR - the perpendicular gradient was wrong - calcualting reciprocal incorrectly, was missing a -
# Spent a loooong time trying to derive the equation for getting the X value for the intercept of a line and a circle
# Got it wrong the first time
# Got it wrong the second time 
# Got confused cause I had a 2nd problem with scaling the circle
# Previously when I was placing the circle o nthe board I was taking hte point, translating it to the board size and then sccaling the radius
# This becomes a problem when trying to track a specific point o nthe circle before and after scaling
# When we expand the circle we dont just multiply each point by the scale factor
# the X,Y of each point is scaled different depending on the angle from the center
# As a result of this When drawing the firing cone points were all over the place
# Had to go back and re-work the scaling to be consistent
# Along with this, The game board uses 0,0 at the top left increasing to the right and down
# This made it difficult to transfer between calculating the values and drawing them
# Spent a while trying to use the method from wolfram alpha - turned out this only worked for circles at 0,0
# Probably couldve just translated the positions there and back but that sounded like a pain
 
 
# 07/04/24
# Old comments remainting for the sake of history - help to write the report 
# Get the line equation of the perpendicular lines
# Get C
# c = y - mx
# chosenOperative.position[1] = perpendicularGradient * chosenOperative.position[0] + c





# Circle equations (x - h)^2 + (y - k)^2 = r^2
# we want to find the intercepts of the line with the circle
# This is a quadratic equation
# (x - h)^2 + (m * x + c - k)^2 = r^2
# x^2 - 2hx + h^2 + (m * x + c - k)^2 = r^2

# dx = chosenOperative.position[0] - operative.position[0]
# dy = chosenOperative.position[1] - operative.position[1]

# dr = sqrt(dx**2 + dy**2)

# capitalD = chosenOperative.position[0] * operative.position[1] - operative.position[0] * chosenOperative.position[1]

# xMinus = (capitalD * dy - self.sgn(dy)*dx * sqrt(chosenOperative.radius**2 * dr**2 - capitalD**2)) / dr**2

# xPlus = (capitalD * dy + self.sgn(dy)*dx * sqrt(chosenOperative.radius**2 * dr**2 - capitalD**2)) / dr**2

# yMinus = (-capitalD * dx - abs(dy) * sqrt(chosenOperative.radius**2 * dr**2 - capitalD**2)) / dr**2

# yPlus = (-capitalD * dx + abs(dy) * sqrt(chosenOperative.radius**2 * dr**2 - capitalD**2)) / dr**2

# self.gameBoard.drawCircle((xMinus,yMinus),2)


# Wolfram testing



# a = 1 + m**2 
# b = c * m - k * m - h
# quadraticC = 2 * k * m * c + c**2 - r**2

# chosenOperativeX = (-b - sqrt(b**2 - (4 * a * quadraticC))) / (2 * a)

# chosenOperativeY = m * chosenOperativeX + c
# print("Chosen Operative")
# print(chosenOperativeX,chosenOperativeY)
# # 514 ish


# print("translated Intersect")
# print(self.gameBoard.translatePointToBoardSize(point=(chosenOperativeX,chosenOperativeY)))
# print("Translated Center")
# print(self.gameBoard.translatePointToBoardSize((chosenOperative.position[0],chosenOperative.position[1])))


# # print(self.gameBoard.translatePointToBoardSize((h,k)))

# self.gameBoard.drawCircle((chosenOperativeX,chosenOperativeY),2)

# self.gameBoard.drawLine((h,k),(operative.position[0],operative.position[1]))






# self.gameBoard.drawCircle((509+ (509-h)*2,490 + (490-k)*2),2)


# self.gameBoard.drawCircle((finalXplus + (finalXplus-h)*2,finalYplus+ (finalYplus-k)*2),2)
# self.gameBoard.drawCircle((finalXminus+ (finalXminus-h)*2,finalYminus+ (finalYminus-k)*2),2)




# This is probably gonna need discriminants :(
# B^2 - 4AC

# -b +- sqrt(b^2 - 4ac) / 2a

# def sgn(self, x):
#     if x < 0:
#         return -1
#     return 1
    
    


# operative 

# 07/04/24
# Actual notes
# LOS - need
# Terrain - need 
# Clicking - need 
# April tags for board corners - would be nice to have
# Realised that pygame rectangles are top left corner based and therefore cant be rotated or placed at an angle
# Can use pygame polygons instead
# Started making terrain representation - realised rectangles won't work so need to re-think solution
# Gonna use polygons instead, need to look at how this should be represented to make my time easier later
# Unfortunatly it would appear im making a very rudamentary game engine as a result of this
#Terrain objects are now polygons - defined as a list of points
# Now we need to check a few things for obscuring 
# We could do this with raycasting but it is way overkill and performance heavy
# It would also give us other problems to deal with (think about what these are at some point)
# instead we will do it mathematically


# Are any of the points of the terrain object within the firing cone
# If yes - Get the point on the lines the point is a part of which is closest to the center of the circle
# Check the distance between the point and the center of the circle - radius of the circle
# If the distance is > 2 inches -> obscured


# If no - are any of the lines of the terrain object intersecting the lines of the firing cone? 
# If yes - return the point on the line closest to the center of the circle


# Vector math - since we have the line of the terrain which is in our line of sight
# For the defender
# we need to find the closest point on the line to our operative (any point in our circle)
# We get the closest point to the center of the circle on the line
# Take the distance and subtract the radius of the circle
# If the distance is > 2 inches -> obscured
# https://gdbooks.gitbooks.io/3dcollisions/content/Chapter1/closest_point_on_line.html
# https://www.varsitytutors.com/hotmath/hotmath_help/topics/shortest-distance-between-a-point-and-a-circle

#08/04/24
# DO THE TERRAIN
# Calibration is gonna be interesting to look at 
# Instead of doing calculations on image space and then translating everything to board space, convert to board space first and then do calculations on that :3
# Wasted an entire day trying to work out why teh firing cone interecepts were when drawn
# I was treating the radius of the circles as the same in both the image space and the board (world) space
# As a result when I was translating the points to the world space The radius of the cricle was remaining the same
# This was causing the firing cone to be drawn in the wrong place
# As a result when performing further calculations a lot of the positions were off as a result
# I really should do a proper translation matrix
# THIS TOOK A WHOLE DAY TO WORK OUT WHAT THE PROBLEM WAS
#

# 09/04/24
# Im not even sure anymore
#  Terrain will now give the lines that each vertex is a member on
#  Terrain is now translated to board space by default
#  Re-working LOS becuase it was a stupid diea
# When doing the terrain positions within the triangle
#  I assumed that the object was entirely within the triangle
# This is obviously not always the case
# Instead I should check if an object is fully within the triangle and then utilise this as an assumption to optimise 
# Previously I was taking a vertex, seeing if it was within the triangle and then checking the 2 lines it was a part of for the closest positio on that line segment to the center of the circle
# If the object was entirely within the triangle this would be fine - If the object is half in half out - then it would return the closest position as outside the triangle (probably)
# INSTEAD
# Check if all the corners are within the triangle -> if they are then we can use the assumption that the object is entirely within the triangle
# Check if all the corners are outside the object -> We can use the assumption that the object is entirely outside the triangle -> find hte intersects -> make lines -> find the closest intersect
# If some corners are in and some are out then we need to build the shape of the object within the triangle

# 2 methods
# 1 - vertex by vertex and then line by line - i.e. take a vertex, check if it is in the triangle, take the 2 connecting vertexes, make the 2 lines, check if they intersect the line of sight
# Construct a line using the original vertex and either the intersect or the connecting vertex
# Get closest point on the line -> see if it satisfies the conditions
# If no vertex within, go line by line to check intercepts -> construct new lines -> get closest point on the line
# repeat until 1 satisfies the conditions
# Upsides - probably quite quick? will give a single yes or no answer
# Downside won't give us all the points that are obstructing the line of sight -> could be useful to display to the user what is obscuring 
# 2 - Construct the shape of the object within the triangle -> Find points in triangle, find all intercepts

# RAYCASTING
# COol idea
# Not gonna work
# Kinda hacky solutiom
# 2 problems
# 1 - performance, would have to do a ray for each point on the circle between the 2 extremes - kinda cringe
# 2 - 2D game board representation - This would probably be quiteeeeeeeeeeeee slow as each terrain piece + model would need to take up a space on the board
# As a 2D array - Since the terrain is defined as a polygon of points. We would need to find a way to fill in the space between the points. THis would probably mean building a software rasteriser
# This is relatively simple to implement BUT PAINFULLY SLOW - we would be doing every pixel for every point for every object - and since this is not multirthreaded or GPU accelerated it would be very slow
# Also the 2D gameboard and the on screen representation would likely differ from eachother so the results returned wouldnt quite be "exact" in our representation
# Unfortanately pygame doesnt have a way to just rip the pixels from the screen given a rect 

#10/04/24
# Probably gonna do some report stuff for today
# Things to do
# Line of sight
# clicking on people
# MAKING VIDEO WORK PLEASE
# Terrain
# (calibration if there is time)

# Spent 2 hours re-doing the LOS
# Tried ot make my own vector library - stupid idea just used numpy
# Tried to find the intersection between a triangle and a line 
# Did the maths for this
# Was getting weird results
# Realised I was defining my triangles from the wrong points 
# but drawing them in the correct place
#  Was probably responsible for some of my previous problems
# This was likely contributing to the problems I was having previously with weird drawing of barycentric coordinates

# Spent a while debugging this -> the stackoverflow guy was annoyingly wrong
# Was only calculating 1 h and taking the solutuon to that - did not actually consider if that complete line 


# 11/04/24
# LOS is the bain of my existence
# Obscuring is now working 
# If an operative is obsured by terrain it will colour that operative yellow
# Now to pu the rest of LOS in
# Had a lot of problems caused by parallel lines and / 0 when computingH 
# Porlbmes in barycentric coordinates caused by rounding errors
# Problems in getting the circle extremes caused by premature rounding
# problems caused by floating point errors when calculating the reciprocal of the gradient
# problems caused by parallel lines when getting the gradient - > had to add some edge cases for this
# Probably shouldve used shapely
# Obscurity now works (hopefully) (havnt done extensive testing but it seems fine)
# The next 2 parts of LOS are cover, concealment and mayyyyyyybe do something about checking "is visable" tho this is somewhat annoying to do


# 12/04/24
# So what do I actually need to do
# Get the video feed working - work out how to put a camera on an arm
# Eligiable to be shot? -> update the visuals to be a bit more descriptive
# Concealment -> update the visuals to be a bit more descriptive
# Talk about UI choices for displaying Line of sight -> display waht is blocking (points) or display the valid sight line -> Obscurity / cover differences? if an object is providing cover do I colour the whole object? or the line?
# TERRAIN FOR THE LOVE OF GOD PLEASE DO TERRAIN
# selecting an operative
# Probably needs some error checking 
# Occlusion is the term we should use for stuff thats blocking -> talk about my solution for occlusion

# April tags are nice to use - well supported - effective - although generating custom ones is a bit of a pain
# OpenCV can do ArUco tags (generate + detect) itself - this is likely the better one to use (cv2.aruco) module
# https://docs.opencv.org/4.x/da/d13/tutorial_aruco_calibration.html
# https://docs.opencv.org/3.4/d5/dae/tutorial_aruco_detection.html
# By the looks of it im probably gonna have to do some calibration :(
# perspectiveRemoveIgnoredMarginPerCell - > When finding the bits in the encoding We should probably take an average of the area inside the bits -> best to ignore areas near the border though
# https://lensfun.github.io/


# Cover - Could just do another loop through for each line of terrain and check if it intersects the line of sight and then check the distances
# Though this feels inefficient
# Instead ->
# We make a function that returns a cover point and an obscuring point (if it exists)


# Refactored the Line of sight code to instead return a list of lines that are within the firing cone
# and then use this list to determine cover obscurity etc