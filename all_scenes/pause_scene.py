import pygame
from scene import Scene
from gui import (Label, Button, Options, Image)
from resources import Resources


class PauseScene(Scene):
    header = None
    back_btn = None
    settings_btn = None

    last_scene_id = -1
    underlay_screen = None

    def start(self, screen):
        if not self.already_loaded:
            width = screen.get_width()
            height = screen.get_height()

            self.header = Label(pygame.rect.Rect(width / 2 - 75, height * 1/5 + 10, 150, 50), "Game Paused", options={
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.BORDER_WIDTH: 0,
            })

            self.back_btn = Button(pygame.rect.Rect(width * 1/5 + 10, height * 1/5 + 10, 60, 40), "Back", {
                Options.BORDER_WIDTH: 0,
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
                Options.FONT: pygame.font.SysFont("Comic Sans MS", 15)
            })

            settings_gear_image = Resources.get("gear")
            settings_gear_rect = pygame.rect.Rect(width * 4/5 - 100, height * 4/5 - 100, 75, 75)
            self.settings_btn = Image(settings_gear_rect, settings_gear_image, {
                Options.BACKGROUND: (20, 61, 89),
                Options.HOVERED_BACKGROUND: (10, 30, 45)
            })

            self.already_loaded = True

        if self.last_scene_id != Scene.scene_stack[-2]:
            self.last_scene_id = Scene.scene_stack[-2]
            self.underlay_screen = screen.copy()
            dark_cover = pygame.Surface(self.underlay_screen.get_size()).convert_alpha()
            dark_cover.fill((0, 0, 0, 0.6 * 255))
            self.underlay_screen.blit(dark_cover, (0, 0))

    def update(self, event):
        for elt in (self.back_btn, self.settings_btn):
            elt.update(event)

        if self.back_btn.clicked:
            Scene.pop_scene()
        elif self.settings_btn.clicked:
            Scene.push_scene(12)

    def draw(self, screen):
        screen.fill((82, 173, 200))
        screen.blit(self.underlay_screen, (0, 0))

        width = screen.get_width()
        height = screen.get_height()

        pygame.draw.rect(screen, (82, 173, 200), pygame.rect.Rect(width * 1/5, height * 1/5, width * 3/5, height * 3/5))

        for elt in (self.header, self.back_btn, self.settings_btn):
            elt.draw(screen)
