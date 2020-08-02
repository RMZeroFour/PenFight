import pygame
from scene import (Scene, SCENE_TRANSITION)
from gui import (Label, Button, Options)
from game_code import PenData
import random


class EnemySelectScene(Scene):
    back_btn = None
    next_btn = None

    def start(self, screen):
        if not self.already_loaded:
            self.back_btn = Button(pygame.rect.Rect(10, 10, 60, 40), "Back", {
                Options.BORDER_WIDTH: 0,
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
                Options.FONT: pygame.font.SysFont("Comic Sans MS", 15)
            })

            self.next_btn = Button(pygame.rect.Rect(200, 50, 60, 40), "Next", {
                Options.BORDER_WIDTH: 0,
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
                Options.FONT: pygame.font.SysFont("Comic Sans MS", 15)
            })

            self.already_loaded = True

    def update(self, event):
        for elt in (self.back_btn, self.next_btn):
            elt.update(event)

        if self.back_btn.clicked:
            Scene.pop_scene()
        elif self.next_btn.clicked:
            PenData.current_enemy_pen = random.choice(PenData.all_pens)
            Scene.push_scene(7)

    def draw(self, screen):
        screen.fill((82, 173, 200))

        for elt in (self.back_btn, self.next_btn):
            elt.draw(screen)
