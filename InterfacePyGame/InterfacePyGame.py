import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 559 * 4
SCREEN_HEIGHT = 381 * 4

# Game board dimensions
BOARD_WIDTH = 559 * 3
BOARD_HEIGHT = 381 * 3

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
def draw_circles(screen, circles):
    for circle in circles:
        pygame.draw.circle(screen, circle['color'], (circle['x'], circle['y']), CIRCLE_RADIUS)

# Main function
def main():
    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Board")

    # Initialize game board rectangle
    game_board_rect = pygame.Rect((SCREEN_WIDTH - BOARD_WIDTH) // 2, 50, BOARD_WIDTH, BOARD_HEIGHT, )

    # Example list of circles
    circles = [{'x': 200, 'y': 150, 'color': RED},
               {'x': 250, 'y': 200, 'color': BLUE}]

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

        # Draw circles on the game board
        draw_circles(screen, circles)

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()
