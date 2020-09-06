import random
import pygame
from scene import Scene
from gui import (Label, Button, ToggleButton, Image, Options)
from resources import Resources
from game_code import PenData
from game_code.strategy import *


class EnemySelectScene(Scene):
    header = None
    back_btn = None

    select_btn = None
    name_text = None

    random_diff_btn = None
    adaptive_btn = None
    offence_btn = None
    defence_btn = None

    random_pen_data = None
    pen_images = []
    visible_pen_images = []
    left_btn, right_btn = None, None

    center_pos = None
    pen_index = 0

    def start(self, screen):
        if not self.already_loaded:
            width = screen.get_width()
            height = screen.get_height()

            self.back_btn = Button(pygame.Rect(10, 10, 60, 40), "Back", {
                Options.BORDER_WIDTH: 0,
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
                Options.FONT: pygame.font.SysFont("Comic Sans MS", 15)
            })

            self.header = Label(pygame.Rect(width / 2 - 200, 10, 400, 30), "Choose your opponent!", {
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.BORDER_WIDTH: 0,
            })

            self.name_text = Label(pygame.Rect(width / 2 - 45, height - 125, 90, 50), "", {
                Options.BACKGROUND: (82, 173, 200),
                Options.FOREGROUND: (20, 61, 89),
                Options.BORDER_WIDTH: 0,
                Options.FONT: pygame.font.SysFont("Comic Sans MS", 18)
            })

            btn_options = {
                Options.BORDER_WIDTH: 0,
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
                Options.FONT: pygame.font.SysFont("Comic Sans MS", 25)
            }
            self.left_btn = Button(pygame.Rect(10, height / 2 - 20, 20, 30), "<", btn_options)
            self.right_btn = Button(pygame.Rect(width - 30, height / 2 - 20, 20, 30), ">", btn_options)
            self.select_btn = Button(pygame.Rect(width / 2 - 45, height - 75, 90, 50), "Select", btn_options)

            btn_options[Options.TOGGLED_BACKGROUND] = (5, 20, 30)
            self.random_diff_btn = ToggleButton(pygame.Rect(width * 1 / 5 - 75, 100, 150, 30), "Random", btn_options)
            self.adaptive_btn = ToggleButton(pygame.Rect(width * 2 / 5 - 75, 100, 150, 30), "Adaptive", btn_options)
            self.offence_btn = ToggleButton(pygame.Rect(width * 3 / 5 - 75, 100, 150, 30), "Offense", btn_options)
            self.defence_btn = ToggleButton(pygame.Rect(width * 4 / 5 - 75, 100, 150, 30), "Defense", btn_options)
            toggle_group = [self.random_diff_btn, self.offence_btn, self.defence_btn, self.adaptive_btn]
            for elt in toggle_group:
                elt.set_group(toggle_group)
            self.adaptive_btn.toggle()

            self.center_pos = pygame.Rect(width / 2 - 50, height / 2 - 50, 100, 100)
            self.random_pen_data = PenData.dict_to_pen({"name": "Random", "image_file": "random_pen"})
            for pen in [self.random_pen_data] + PenData.all_pens:
                self.pen_images.append(Image(self.center_pos, Resources.get(pen.image_file), {
                    Options.BACKGROUND: (82, 173, 200)
                }))

            self.already_loaded = True

        self.reposition_images()
        self.update_enemy_data()

    def update(self, event):
        for elt in (self.back_btn, self.left_btn, self.right_btn, self.select_btn,
                    self.random_diff_btn, self.offence_btn, self.defence_btn, self.adaptive_btn):
            elt.update(event)

        if self.select_btn.clicked:
            PenData.current_enemy_pen = \
                random.choice(PenData.all_pens) if self.pen_index == 0 else \
                PenData.all_pens[self.pen_index - 1]

            possible_strategies = [hybrid_strategy, offensive_strategy, defensive_strategy]
            PenData.current_enemy_strategy = \
                possible_strategies[0] if self.adaptive_btn.toggled else \
                possible_strategies[1] if self.offence_btn.toggled else \
                possible_strategies[2] if self.defence_btn.toggled else \
                random.choice(possible_strategies)

            Scene.push_scene(7)

        if self.back_btn.clicked:
            Scene.pop_scene()

        if self.left_btn.clicked or self.right_btn.clicked:
            if self.left_btn.clicked:
                self.pen_index -= 1
                self.reposition_images()
            elif self.right_btn.clicked:
                self.pen_index += 1
                self.reposition_images()
            self.update_enemy_data()

    def reposition_images(self):
        self.visible_pen_images.clear()

        if self.pen_index > 0:
            img = self.pen_images[self.pen_index - 1]
            self.visible_pen_images.append(img)
            img.rect = self.center_pos.copy().move(-300, 40)

        self.visible_pen_images.append(self.pen_images[self.pen_index])
        self.pen_images[self.pen_index].rect = self.center_pos

        if self.pen_index < len(self.pen_images) - 1:
            img = self.pen_images[self.pen_index + 1]
            self.visible_pen_images.append(img)
            img.rect = self.center_pos.copy().move(300, 40)

        self.left_btn.set_enabled(self.pen_index > 0)
        self.right_btn.set_enabled(self.pen_index < len(self.pen_images) - 1)

    def update_enemy_data(self):
        self.name_text.text = self.random_pen_data.name if self.pen_index == 0 else \
            PenData.all_pens[self.pen_index - 1].name
        self.name_text.recreate()

    def draw(self, screen):
        screen.fill((82, 173, 200))

        for elt in (self.header, self.back_btn, self.left_btn, self.right_btn, self.name_text, self.select_btn,
                    self.offence_btn, self.defence_btn, self.adaptive_btn, self.random_diff_btn):
            elt.draw(screen)

        for img in self.visible_pen_images:
            img.draw(screen)
