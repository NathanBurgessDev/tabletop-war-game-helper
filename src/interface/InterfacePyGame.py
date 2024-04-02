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

# Screen dimensions
SCREEN_WIDTH = 559 * 4
SCREEN_HEIGHT = 381 * 4

# Game board dimensions
BOARD_WIDTH = 559 * 3 # 1677
BOARD_HEIGHT = 381 * 3 # 1143

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Circle radius
# Spent a while being confused - found out I was using radius not diameter
CIRCLE_RADIUS = 14 * 3

class GameBoard:
    def __init__(self,imageSize ):
        self.imageSize = imageSize

    # Function to draw circles on the game board
    # def draw_circles(self, screen, circles, imageSize):
    #     for circle in circles:
    #         pygame.draw.circle(screen, RED, translateToBoardSize(circle.circleCenter,imageSize), CIRCLE_RADIUS)
            
    def drawOperative(self, screen, operative: Operative,):
        pygame.draw.circle(screen, operative.getColourRGB(), self.translateToBoardSize(operative.position), operative.radius * 3)
        # Draw the name of the operative
        font = pygame.font.Font(None, 36)
        text = font.render(operative.name, True, WHITE)
        screen.blit(text, self.translateToBoardSize(operative.position))

    # This took a while to get working
    # We need to translate the circle center from the size of the image to the size of the baord
    # To do this we need to use a scale factor to translate the circle center and then move it to be relative to the 0,0 of the board display
    # As opposed to the 0,0 of the screen
    # Spent a while on this cause imageSize is in the format (height, width) and I was using it as (width, height)
    def translateToBoardSize(self, circleCenter):
        newCenterWidth = (circleCenter[0] * (BOARD_WIDTH / self.imageSize[1])) + ((SCREEN_WIDTH - BOARD_WIDTH) // 2)
        newCenterHeight = (circleCenter[1] * (BOARD_HEIGHT / self.imageSize[0])) + 50
        return (newCenterWidth, newCenterHeight)



# Main function
def startMainInterface():
    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Board")

    # Initialize game board rectangle
    game_board_rect = pygame.Rect((SCREEN_WIDTH - BOARD_WIDTH) // 2, 50, BOARD_WIDTH, BOARD_HEIGHT, ) ## 0,0 for the game board is (SCREEN_WIDTH - BOARD_WIDTH) // 2, 50
    
    # Creates our list of operatives with the ID's in use
    operativeList = OperativeList()
    
    
    
    # Calibrate the top down view (currently just using an image for testing)
    filePath = "testImages/paperTestCorners.jpg"
    
    image = cv.imread(filePath)
    
    image = cv.rotate(image, cv.ROTATE_90_CLOCKWISE)
    
    modelFinder = ModelFinder(image)
    
    

    gameBoardData = modelFinder.identifyModels(image, modelFinder.cornerPoints)
    # print(gameBoardData)
    
    
    # circles = identifyAllPieces()

    imageSize = gameBoardData[1]
    
    gameBoard = GameBoard(imageSize)
    
    operativeList.updateEncodingListPositions(gameBoardData[0])

    # Main loop
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(GRAY)

        # Draw the game board rectangle
        pygame.draw.rect(screen, BLACK, game_board_rect)
        # Center of the game board
        pygame.draw.circle(screen, BLUE,(((SCREEN_WIDTH - BOARD_WIDTH) // 2) + (BOARD_WIDTH // 2),(BOARD_HEIGHT // 2) + 50), 10)



        # Draw operatives on the game board        
        for operative in operativeList.encodings:
            gameBoard.drawOperative(screen, operative)

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    startMainInterface()



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
# 2.1 storing the game state in a 2D array to show operative positions and terrain
# 3. Get movement of operatives working
# 4. Next turn button
# 5. Get RayCasting working (primative terrain) 
# 6. Terrain


# 02/04/24
# Droidcam / Irun webcam
# If I want to use a proper camera I need a capture card
# Droidcam may only be SD output not HD
# Irun is only for ubuntu 
# Droidcam: v4l2loopback-dc fails to compile on kernels 6.8+
# Patched 2 weeks ago - supposbly merged to main branch but doesnt seem to be working
# Continunity Camera
# Logitech webcam now works with good framerate - however only 1080p :(
# sudo modprobe v4l2loopback fixed the problem - kernal update
# Getting 1920x1080 input from webcam is very very slow - this is an openCV problem, works fine in OBS or Kamoso
# Getting webcam input can be difficult - /dev/video?
# Where ? is the number of the camera, we would pass /dev/video0 for the default camera
# for some reason video1 always fails and video2 is our "other" camera
# droidcam will take over video2 though webcam can sometimes take over video0
# Spent some time refactoring the code to let calibration be more easily done, storing the corner points in an object so we can use them for each image (part of getting video working)