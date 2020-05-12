# Import and initialize the pygame library
import pygame
pygame.init()

# Import the scenes for the game
import scene
import all_scenes

# Set up the game window
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pygame Test")

# Set a delay and repeat timer for keyboard input
pygame.key.set_repeat(300, 100)

# Create all the scenes of the game
scenes = {
    0: all_scenes.LoadingScene(),
    1: all_scenes.MainMenuScene(),
    2: all_scenes.EnemySelectScene(),
    3: all_scenes.PenSelectScene(),
    4: all_scenes.GameScene(),
    5: all_scenes.PauseScene(),
    6: all_scenes.GameOverScene(),
    7: all_scenes.AboutScene(),
}

# Select the first scene as current and load it
current_scene = scenes[0]
current_scene.start(WINDOW_WIDTH, WINDOW_HEIGHT)

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
            current_scene.start(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Update the current scene
        else: 
            current_scene.update(event) 
    
    # Draw the current scene
    current_scene.draw(screen)

    # Display the graphics
    pygame.display.flip()

# Done! Time to quit
pygame.quit()