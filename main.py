# Import and initialize the pygame library
import pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pygame Test")

# Run until the window closes
finished = False
while not finished:

    # Check is the user clicks the window close button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Display the graphics
    pygame.display.flip()

# Done! Time to quit
pygame.quit()