import pygame
import sys
import cv2 as cv

# from pathlib import Path
import path
# path_root = Path(__file__).parents[2]
# print(path_root)
# sys.path.append('../')
direction = path.Path(__file__).abspath()
sys.path.append(direction.parent.parent)
from markerIdentfication.combined import ModelFinder
from modelEncodings.encodingsInUse import Operative, OperativeList

# Initialize Pygame
pygame.init()

# Scaling
SCREEN_SCALE = 4
BOARD_SCALE = 3

# Screen dimensions
SCREEN_WIDTH = 559 * SCREEN_SCALE
SCREEN_HEIGHT = 381 * SCREEN_SCALE

# Game board dimensions
BOARD_WIDTH = 559 * BOARD_SCALE # 1677
BOARD_HEIGHT = 381 * BOARD_SCALE # 1143

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Circle radius
# Spent a while being confused - found out I was using radius not diameter
CIRCLE_RADIUS = 14 * BOARD_SCALE

class GameBoard:
    gameBoardRect = pygame.Rect((SCREEN_WIDTH - BOARD_WIDTH) // 2, 50, BOARD_WIDTH, BOARD_HEIGHT)
    
    def __init__(self,screen,imageSize = (0,0)):
        if (imageSize == (0,0)):
            self.setTestMode()
            self.screen = screen
        else:
            self.imageSize = imageSize
            self.screen = screen
            
    def drawOperative(self, screen, operative: Operative,):
        pygame.draw.circle(screen, operative.getColourRGB(), self.translatePointToBoardSize(operative.position), operative.radius * BOARD_SCALE)
        # Draw the name of the operative
        font = pygame.font.Font(None, 36)
        text = font.render(operative.name, True, WHITE)
        screen.blit(text, self.translateCircleToBoardSize(operative.position))

    # This took a while to get working
    # We need to translate the circle center from the size of the image to the size of the baord
    # To do this we need to use a scale factor to translate the circle center and then move it to be relative to the 0,0 of the board display
    # As opposed to the 0,0 of the screen
    # Spent a while on this cause imageSize is in the format (height, width) and I was using it as (width, height)
    def translatePointToBoardSize(self, point: tuple[int,int]) -> tuple[int,int]:
        newCenterWidth = (point[0] * (BOARD_WIDTH / self.imageSize[1])) + ((SCREEN_WIDTH - BOARD_WIDTH) // 2)
        newCenterHeight = (point[1] * (BOARD_HEIGHT / self.imageSize[0])) + 50
        return (newCenterWidth, newCenterHeight)
    
    def setTestMode(self):
        self.imageSize = (381 * BOARD_SCALE,559 * BOARD_SCALE)
        
    def drawGameBoard(self):
        pygame.draw.rect(self.screen, BLACK, self.gameBoardRect)
        # Center of the game board
        pygame.draw.circle(self.screen, BLUE,(((SCREEN_WIDTH - BOARD_WIDTH) // 2) + (BOARD_WIDTH // 2),(BOARD_HEIGHT // 2) + 50), 10)
        




class MainGame:
    def __init__(self, operativeList: OperativeList, testing: bool):
        self.operativeList = operativeList
        self.testingFlag = testing
        self.setupScreen()
        if (testing):
            self.setupModelFinderTesting()
            self.setupGameBoardTesting()
        else:
            self.setupModelFinder()
            self.setupGameBoard()
        self.gameLoop()
        
    def setupModelFinder(self):
        filePath = "testImages/paperTestCorners.jpg"
        
        image = cv.imread(filePath)
        image = cv.rotate(image, cv.ROTATE_90_CLOCKWISE)
        
        self.modelFinder = ModelFinder(image)
        gameBoardData = self.modelFinder.identifyModels(image, self.modelFinder.cornerPoints)
        self.imageSize = gameBoardData[1]
        
    def setupModelFinderTesting(self):
        pass
            
    
    def setupScreen(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game Board")
        
    def setupGameBoard(self):
        self.gameBoard = GameBoard(screen=self.screen,imageSize=self.imageSize)
        
    def setupGameBoardTesting(self):
        self.gameBoard = GameBoard(screen=self.screen)
        
        
    def gameLoop(self):
        
        # Testing purposes we do an inital update
        if (not self.testingFlag):
        
            filePath = "testImages/paperTestCorners.jpg"
            
            image = cv.imread(filePath)
            image = cv.rotate(image, cv.ROTATE_90_CLOCKWISE)
            
            gameBoardData = self.modelFinder.identifyModels(image,self.modelFinder.cornerPoints)
            
            if (gameBoardData[0] != None):
                operativeList.updateEncodingListPositions(gameBoardData[0])
            
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            # Clear the screen
            self.screen.fill(GRAY)

            # Draw the game board
            self.gameBoard.drawGameBoard()

            # Draw operatives on the game board        
            for operative in self.operativeList.encodings:
                self.gameBoard.drawOperative(self.screen, operative)

            # Update the display
            pygame.display.flip()
        
        

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