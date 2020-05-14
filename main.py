# Import and initialize the pygame library
import pygame
pygame.init()

# Import the accounts i/o
from account import Account

# Import the scenes for the game
from scene import SCENE_TRANSITION
import all_scenes

# Set up the game window
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Python Penfight!")

# Set a delay and repeat timer for keyboard input
pygame.key.set_repeat(300, 100)

# Create all the scenes of the game
scenes = {
    0: all_scenes.LoadingScene(),
    1: all_scenes.SelectAccountScene(),
    2: all_scenes.CreateAccountScene(),
    3: all_scenes.DeleteAccountScene(),
    4: all_scenes.MainMenuScene(),
    5: all_scenes.EnemySelectScene(),
    6: all_scenes.PenSelectScene(),
    7: all_scenes.GameScene(),
    8: all_scenes.PauseScene(),
    9: all_scenes.GameOverScene(),
    10: all_scenes.StatsScene(),
    11: all_scenes.AboutScene(),
    12: all_scenes.SettingsScene(),
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
        elif event.type == SCENE_TRANSITION:
            current_scene = scenes[event.next_scene_id]
            current_scene.start(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Update the current scene
        else:
            current_scene.update(event)

            # Draw the current scene
    current_scene.draw(screen)

    # Display the graphics
    pygame.display.flip()

# Save the account details, just in case
Account.save_to_file(Account.current_account)

# Done! Time to quit
pygame.quit()
