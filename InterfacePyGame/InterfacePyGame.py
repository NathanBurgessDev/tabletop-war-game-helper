import pygame
import sys

from pathlib import Path
path_root = Path(__file__).parents[2]
print(path_root)
sys.path.append(str(path_root) + "/Diss")
from Detection.combined import identifyAllPieces

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

# Function to draw circles on the game board
def draw_circles(screen, circles, imageSize):
    for circle in circles:
        pygame.draw.circle(screen, RED, translateToBoardSize(circle.circleCenter,imageSize), CIRCLE_RADIUS)

# This took a while to get working
# We need to translate the circle center from the size of the image to the size of the baord
# To do this we need to use a scale factor to translate the circle center and then move it to be relative to the 0,0 of the board display
# As opposed to the 0,0 of the screen
# Spent a while on this cause imageSize is in the format (height, width) and I was using it as (width, height)
def translateToBoardSize(circleCenter, imageSize):
    newCenterWidth = (circleCenter[0] * (BOARD_WIDTH / imageSize[1])) + ((SCREEN_WIDTH - BOARD_WIDTH) // 2)
    newCenterHeight = (circleCenter[1] * (BOARD_HEIGHT / imageSize[0])) + 50
    return (newCenterWidth, newCenterHeight)


# Main function
def main():
    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Board")

    # Initialize game board rectangle
    game_board_rect = pygame.Rect((SCREEN_WIDTH - BOARD_WIDTH) // 2, 50, BOARD_WIDTH, BOARD_HEIGHT, ) ## 0,0 for the game board is (SCREEN_WIDTH - BOARD_WIDTH) // 2, 50

    gameBoardData = identifyAllPieces()
    # circles = identifyAllPieces()
    circles = gameBoardData[0]
    imageSize = gameBoardData[1]
    print(imageSize)
    print ((BOARD_WIDTH / imageSize[1]))
    print((BOARD_HEIGHT / imageSize[0]))

    # Main loop
    while True:
        # print("event happening")
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(GRAY)

        # Draw the game board rectangle
        pygame.draw.rect(screen, BLACK, game_board_rect)
        pygame.draw.circle(screen, BLUE,(((SCREEN_WIDTH - BOARD_WIDTH) // 2) + (BOARD_WIDTH // 2),(BOARD_HEIGHT // 2) + 50), 10)

        # Draw circles on the game board
        draw_circles(screen, circles, imageSize)

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()



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