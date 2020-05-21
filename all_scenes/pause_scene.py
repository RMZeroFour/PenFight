import pygame
from scene import Scene
from gui import (Label, Button, Options, Image)
from resources import Resources


class PauseScene(Scene):
    header = None
    back_btn = None
    settings_btn = None

    def start(self, width, height):
        if not self.already_loaded:
            self.header = Label(pygame.rect.Rect(width / 2 - 50, 10, 150, 50), "Game Paused", options={
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.BORDER_WIDTH: 0,
            })

            self.back_btn = Button(pygame.rect.Rect(10, 10, 60, 40), "Back", {
                Options.BORDER_WIDTH: 0,
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
                Options.FONT: pygame.font.SysFont("Comic Sans MS", 15)
            })

            settings_gear_image = Resources.get("gear")
            settings_gear_rect = pygame.rect.Rect(width - 100, height - 100, 75, 75)
            self.settings_btn = Image(settings_gear_rect, settings_gear_image, {
                Options.BACKGROUND: (20, 61, 89)
            })

            self.already_loaded = True

    def update(self, event):
        for elt in (self.back_btn, self.settings_btn):
            elt.update(event)

        if self.back_btn.clicked:
            Scene.change_scene(7)
        elif self.settings_btn.clicked:
            Scene.change_scene(12)

    def draw(self, screen):
        screen.fill((82, 173, 200))

        for elt in (self.header, self.back_btn, self.settings_btn):
            elt.draw(screen)
