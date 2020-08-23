# Import and initialize the pygame library
import pygame
pygame.init()

# Import the accounts i/o
from account import Account

# Import the scenes for the game
from scene import (Scene, SCENE_TRANSITION)
import all_scenes


# Set up the game window
screen = pygame.display.set_mode((1300, 700))
pygame.display.set_caption("Python PenFight!")

# Set a delay and repeat timer for keyboard input
pygame.key.set_repeat(300, 100)

# Create all the scenes of the game
scenes = {
    0: all_scenes.LoadingScene(),
    1: all_scenes.SelectAccountScene(),
    2: all_scenes.CreateAccountScene(),
    3: all_scenes.DeleteAccountScene(),
    4: all_scenes.MainMenuScene(),
    5: all_scenes.PenSelectScene(),
    6: all_scenes.EnemySelectScene(),
    7: all_scenes.GameScene(),
    8: all_scenes.PauseScene(),
    9: all_scenes.ForfeitScene(),
    10: all_scenes.GameOverScene(),
    11: all_scenes.StatsScene(),
    12: all_scenes.AboutScene(),
    13: all_scenes.SettingsScene(),
}

# Push the first scene onto the scene stack
Scene.scene_stack.append(0)

# Select the first scene as current and load it
current_scene = scenes[Scene.scene_stack[-1]]
current_scene.start(screen)

# Run until the window closes
finished = False
while not finished:

    # Check is the user clicks the window close button
    for event in pygame.event.get():
        # Check for exit
        if event.type == pygame.QUIT:
            finished = True

        # Also check for Alt+F4
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and pygame.key.get_mods() & pygame.KMOD_ALT:
            finished = True

        # Check for scene transition
        elif event.type == SCENE_TRANSITION:
            current_scene = scenes[Scene.scene_stack[-1]]
            current_scene.start(screen)

        # Update the current scene
        else:
            current_scene.update(event)

    # Draw the current scene
    current_scene.draw(screen)

    # Display the graphics
    pygame.display.flip()

# Save the account details, just in case
if Account.current_account is not None:
    Account.save_to_file(Account.current_account)

# Done! Time to quit
pygame.quit()
