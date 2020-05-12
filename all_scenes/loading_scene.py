import pygame
from scene import Scene
from resources import Resources
from gui import (Label, Options)
from threading import Thread
from time import sleep


class LoadingScene(Scene):
    loaded = False
    loading_text = None

    def start(self, width, height):
        # Spawn a new thread to load all resources
        Thread(target=self.load_assets).start()

        # Meanwhile create a label to show that the game is loading
        text_rect = pygame.rect.Rect(width / 2 - 100, height / 2 - 50, 200, 100)
        self.loading_text = Label(text_rect, "Loading...", {
            Options.BACKGROUND: (20, 61, 89),
            Options.FOREGROUND: (244, 180, 26),
            Options.BORDER_WIDTH: 0,
        })

    def load_assets(self):
        # ...ASSET LOADING CODE HERE...
        sleep(2) # Simulate loading assets with a thread sleep
        self.loaded = True

    def update(self, event):
        # Nothing to update here
        return

    def draw(self, screen):
        screen.fill((82, 173, 200))

        # Wait if the loading has not finished
        if not self.loaded:
            self.loading_text.draw(screen)

        # If loading has finished, then go to main menu
        else:
            Scene.change_scene(1)
