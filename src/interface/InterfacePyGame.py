import pygame
import numpy as np
import sys
import cv2 as cv
from math import sqrt

import path
import time

direction = path.Path(__file__).abspath()
sys.path.append(direction.parent.parent)
from markerIdentfication.combined import ModelFinder
from modelEncodings.encodingsInUse import Operative, OperativeList
from terrain.TerrainObject import Terrain, TerrainLine, PillarDoubleWall
from camera.Camera import Camera

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
LIGHT_GRAY = (211, 211, 211)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)


CIRCLE_RADIUS = 14 * BOARD_SCALE

class BarycentricCoordinates:
    def __init__(self,alpha,beta,gamma):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
'''
Class for handling the game board.
Deals with the drawing of the game board and translating to the correct coordinates.
'''
class GameBoard:
    gameBoardRect = pygame.Rect((SCREEN_WIDTH - BOARD_WIDTH) // 2, 50, BOARD_WIDTH, BOARD_HEIGHT)
    imageInch = None
    concealedImage = pygame.image.load("assets/concealed-icon.png")
    concealedImageCenter = (concealedImage.get_width() // 2, concealedImage.get_height() // 2)
    
    engagedImage = pygame.image.load("assets/engaged-icon.png")
    engagedImageCenter = (engagedImage.get_width() // 2, engagedImage.get_height() // 2)
    terrainList = []
    def __init__(self,screen,imageSize = (0,0)):
        if (imageSize == (0,0)):
            self.setTestMode()
            self.screen = screen
        else:
            self.imageSize = imageSize
            self.screen = screen
        
        
    '''
    Draws operatives based on the provided operative object
    
    '''
    def drawOperative(self, operative: Operative):
        
        if (operative.selected):
            pygame.draw.circle(self.screen, LIGHT_GRAY, operative.position, operative.radius+5)
        
        if (operative.obsured and operative.inCover):
            pygame.draw.circle(self.screen, GREEN, operative.position, operative.radius)
            pygame.draw.circle(self.screen, operative.getColourRGB(), operative.position, operative.radius-5)
            
        elif (operative.obsured):
            pygame.draw.circle(self.screen, YELLOW, operative.position, operative.radius)
            pygame.draw.circle(self.screen, operative.getColourRGB(), operative.position, operative.radius-5)
            
        elif (operative.inCover):
            pygame.draw.circle(self.screen, ORANGE, operative.position, operative.radius)
            pygame.draw.circle(self.screen, operative.getColourRGB(), operative.position, operative.radius-5)
            
        else:
            pygame.draw.circle(self.screen, operative.getColourRGB(), operative.position, operative.radius)
            
        if (operative.concealed):
            self.screen.blit(self.concealedImage, (operative.position[0] - self.concealedImageCenter[0],operative.position[1]- self.concealedImageCenter[1]))
        else:
            self.screen.blit(self.engagedImage, (operative.position[0]- self.engagedImageCenter[0],operative.position[1] - self.engagedImageCenter[1]))
        
        font = pygame.font.Font(None, 36)
        text = font.render(operative.name, True, WHITE)
        text_rect = text.get_rect(center = (operative.position[0], operative.position[1] - operative.radius - 10))
        self.screen.blit(text, text_rect)
        return 
    
    def drawRemoveButton(self, rect: pygame.rect.Rect):
        pygame.draw.rect(self.screen, RED, rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Remove Operative", True, WHITE)
        self.screen.blit(text, (rect.x + 10, rect.y + 10))
        
    def drawSwapStateButton(self, rect: pygame.rect.Rect):
        pygame.draw.rect(self.screen, RED, rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Swap State", True, WHITE)
        self.screen.blit(text, (rect.x + 10, rect.y + 10))
        
    def drawSelectedOperative(self,operative: Operative):
        pygame.draw.circle(self.screen, operative.getColourRGB(), operative.position, operative.radius)
        pygame.draw.circle(self.screen, operative.getColourRGB(), operative.position, operative.radius - 5)
        
        # Draw the name of the operative
        font = pygame.font.Font(None, 36)
        text = font.render(operative.name, True, WHITE)
        self.screen.blit(text, operative.position)
        
    def drawOperativeObscured(self, operative: Operative):
        pygame.draw.circle(self.screen, YELLOW, operative.position, operative.radius)
        
        pygame.draw.circle(self.screen, operative.getColourRGB(), operative.position, operative.radius - 5)
        
        font = pygame.font.Font(None, 36)
        text = font.render(operative.name, True, WHITE)
        self.screen.blit(text, operative.position)
        
    
        
    def drawCircle(self, circle: tuple[int,int], radius: int):
        pygame.draw.circle(self.screen, MAGENTA, (int(circle[0]),int(circle[1])), radius)
        
    def drawYellowCircle(self, circle: tuple[int,int], radius: int):
        pygame.draw.circle(self.screen, YELLOW, (int(circle[0]),int(circle[1])), radius)
        
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
        # print(((SCREEN_WIDTH - BOARD_WIDTH) // 2))
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
        
                
            


'''
Main game object
Stores the game board and the list of operatives
Handles the main game loop
'''
class MainGame:
    
    '''
    Performs the initial setup of the game
    If testing is true then the game will run in testing mode
    This disables the camera and uses a static image
    '''
    def __init__(self, operativeList: OperativeList, testing: bool):
        self.gameBoard: GameBoard = None
        self.operativeList = operativeList
        self.testingFlag = testing
        self.camera = Camera(2)
        self.setupScreen()
        self.currentFrame = self.camera.getFrame()
        self.removeOperativeButton = pygame.rect.Rect(300, 1200, 250, 50)
        self.swapOperativeState = pygame.rect.Rect(300, 1300, 250, 50)
        self.currentOperativeId = None
        if (testing):
            self.setupModelFinderTesting()
            self.setupGameBoardTesting()
        else:
            imageSize = self.setupModelFinder()
            self.setupGameBoard(imageSize)
        self.gameLoop()
        
    def setupModelFinder(self):
        
        self.modelFinder = ModelFinder(self.currentFrame)
        gameBoardData = self.modelFinder.identifyModels(self.currentFrame)
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
        
    def updateOperativeData(self):
        gameBoardData = self.modelFinder.identifyModels(self.currentFrame)
        self.gameBoard.imageSize = gameBoardData[1]
        
        if (gameBoardData[0] != None):
            for operative in gameBoardData[0]:
                operative.circleCenter = self.gameBoard.translatePointToBoardSize(operative.circleCenter)
            self.operativeList.updateEncodingListPositions(gameBoardData[0])
                
    
    
    '''
    Updates the terrain in the game
    This takes the data returned from terrain tracking and then builds new terrain objects or updates existing ones
    '''     
    def updateTerrainData(self):
         if (not self.testingFlag):
            terrainData = self.modelFinder.identifyTerrain(self.currentFrame)
            if (terrainData != None):
                for terrain in terrainData:
                    doesExist = False
                    # If the terrain ID is already in the list we don't want to add it again
                    # Just update the position
                    for i, existingTerrain in enumerate(self.gameBoard.terrainList):
                        if (existingTerrain.id == terrain.id):
                            if (terrain.rotation == existingTerrain.angle + 3 or terrain.rotation == existingTerrain.angle - 3):
                                continue
                            if (terrain.id <= 10):
                                newTerrain = PillarDoubleWall(terrain.id)
                       
                                newTerrain.rotatePolygon(terrain.rotation)
                                newTerrain.angle = terrain.rotation
                                newTerrain.scalePolygon(3,3)
                            
                                translation = newTerrain.findXandYTranslation(self.gameBoard.translatePointToBoardSize(terrain.cornerPointsAsTupleList[3]),newTerrain.verticies[0])
                                newTerrain.translatePolygon(translation[0],translation[1])
                                
                                # for vertex in newTerrain.verticies:
                                #     newTerrain.verticies[newTerrain.verticies.index(vertex)] = self.gameBoard.translatePointToBoardSize(vertex)
                                    
                                newTerrain.updatePolygon()
                                self.gameBoard.terrainList[i] = newTerrain
                                doesExist = True
                                continue
                        
                    if (terrain.id <= 10 and not doesExist):
                        
                        newTerrain = PillarDoubleWall(terrain.id)
                       
                        newTerrain.rotatePolygon(terrain.rotation)
                        newTerrain.angle = terrain.rotation
                        newTerrain.scalePolygon(3,3)
                    
                        translation = newTerrain.findXandYTranslation(self.gameBoard.translatePointToBoardSize(terrain.cornerPointsAsTupleList[3]),newTerrain.verticies[0])
                        newTerrain.translatePolygon(translation[0],translation[1])
                        # print(newTerrain.verticies[0])
                        
                        # for vertex in newTerrain.verticies:
                        #     newTerrain.verticies[newTerrain.verticies.index(vertex)] = self.gameBoard.translatePointToBoardSize(vertex)
                            
                        newTerrain.updatePolygon()

                        # newTerrain.rotatePolygon(terrain.rotation)
                        self.gameBoard.addTerrain(newTerrain)
                    
    
                
 
                    
        
        
        
        
    ''' Main Game loop
    - Handles events
    - Updates the current camera frame
    - Does the operative and terrain checking with the camera frame
    - Updates the operatives and their positions
    - Draws everything to the board except operatives
    - Checks for line of sight on the selected operative
    - Draws the line of sight
    - Draws the operative
    '''
    def gameLoop(self):    
        
        if (not self.testingFlag):
            self.updateOperativeData()
            self.updateTerrainData()
       
        
        while True:
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.camera.release()
                    cv.destroyAllWindows()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handleOnClick(event)

            
            self.currentFrame = self.camera.getFrame()
            
            if (not self.testingFlag):
                self.updateOperativeData()
                self.updateTerrainData()
            

            for operative in self.operativeList.operatives:
                operative.obsured = False
                operative.inCover = False

            # Clear the screen
            self.screen.fill(GRAY)

            # Draw the game board
            self.gameBoard.drawGameBoard()
            
            # Draw any buttons
            self.gameBoard.drawRemoveButton(self.removeOperativeButton)
            self.gameBoard.drawSwapStateButton(self.swapOperativeState)
            
            #Draw terrain
            self.gameBoard.drawTerrain()
            
            # print(self.currentOperativeId)
    
            self.checkLineOfSight(self.currentOperativeId)
            
                

            # Draw operatives on the game board        
            for operative in self.operativeList.operatives:
                    self.gameBoard.drawOperative(operative)
                    # print(operative.position)
                    
            
            
           
            # Update the display
            pygame.display.flip()
            
    
   
    def handleOnClick(self,event):
        if (self.removeOperativeButton.collidepoint(event.pos)):
            self.operativeList.removeOperative(self.currentOperativeId)
            self.currentOperativeId = None
            return
        
        if (self.swapOperativeState.collidepoint(event.pos)):
            self.operativeList.swapOperativeState(self.currentOperativeId)
            return
        
        for operative in self.operativeList.operatives:
            operativeBase = pygame.rect.Rect(operative.position[0] - operative.radius,operative.position[1] - operative.radius,operative.radius * 2,operative.radius * 2)
            if (operativeBase.collidepoint(event.pos)):
                self.currentOperativeId = operative.id
                self.operativeList.resetOperativeSelection()
                operative.selected = True
                break
            
    # Draw 2 Firing cones from the extreme of each circle to the extremes of the other circle
    # Get the gradient of the line between the two circles
    # Take the negative of the gradient to get the perpendicular gradient
    # For each circle
    # Get the intercepts of the perpendicular lines with the circle
    # Draw a triangle between these three points
    def checkLineOfSight(self, operativeID):
        if operativeID == None:
            return
        chosenOperative = self.operativeList.getModelById(operativeID)
     
        for operative in self.operativeList.operatives:
            if (chosenOperative.team != operative.team):
             
                
                chosenOperativePoints = self.getCircleExtremes(chosenOperative.position[0],chosenOperative.position[1],chosenOperative.radius,operative.position[0],operative.position[1])
                
                targetOperativePoints = self.getCircleExtremes(operative.position[0],operative.position[1],operative.radius,chosenOperative.position[0],chosenOperative.position[1])
        
       
                
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
                    self.operativeList.setOperativeToInCover(operative.id)
                
                        
                            
 
   
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


             
                if (distanceToDefender >= BOARD_INCH*2 and distanceToShooter >= BOARD_INCH):
                   
                    self.gameBoard.drawCircle(closestPointDefender,5)
                    return True
                if (distanceToDefender1 >= BOARD_INCH*2 and distanceToShooter1 >= BOARD_INCH):
                 
                    self.gameBoard.drawCircle(closestPointAttacker,5)
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
    '''
    Handles the creation of a list of lines within the firing cone.
    '''
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
    
    # Used in getting line segment intercepts
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
        
        return ((finalXminus,finalYminus),(finalXplus,finalYplus))
    

if __name__ == "__main__":
    operativeList = OperativeList()
    game = MainGame(operativeList = operativeList,testing = True)






