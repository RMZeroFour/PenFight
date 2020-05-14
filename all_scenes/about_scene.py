import pygame
from scene import (Scene, SCENE_TRANSITION)
from gui import (Label, Button, Options)
from random import random
from settings import Settings

class AboutScene(Scene):
    back_btn = None

    def start(self, width, height):
        if not self.already_loaded:
            self.back_btn = Button(pygame.rect.Rect(10, 10, 60, 40), "Back", {
                Options.BORDER_WIDTH: 0,
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
                Options.FONT: pygame.font.SysFont("Comic Sans MS", 15)
            })

            self.already_loaded = True

    def update(self, event):
        self.back_btn.update(event)

        if self.back_btn.clicked:
            Scene.change_scene(4)

    def draw(self, screen):
        screen.fill((82, 173, 200))
        self.back_btn.draw(screen)
