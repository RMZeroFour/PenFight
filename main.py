# Import and initialize the pygame library
import pygame
pygame.init()

# Import the custom gui elements
import gui

# Import the scenes for the game
import scene

# Set up the game window
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pygame Test")

# Create all the scenes of the game
scenes = {
    0: scene.TestScene1(),
    1: scene.TestScene2(),
    2: scene.TestScene3()
}

# Select the first scene as current
current_scene = scenes[0]

# Run until the window closes
finished = False
while not finished:

    # Check is the user clicks the window close button
    for event in pygame.event.get():
        # Check for exit
        if event.type == pygame.QUIT:
            finished = True

        # Check for scene change
        elif event.type == scene.SCENE_TRANSITION:
            next_scene_id = event.next_scene_id
            current_scene = scenes[next_scene_id]

        # Update the current scene
        else: 
            current_scene.update(event) 
    
    # Draw the current scene
    current_scene.draw(screen)

    # Display the graphics
    pygame.display.flip()

# Done! Time to quit
pygame.quit()