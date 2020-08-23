import random
import pygame
from scene import Scene
from gui import (Label, Button, ToggleButton, Image, Options)
from resources import Resources
from game_code import PenData, AIData
from game_code.ai_data import AIDifficulty


class EnemySelectScene(Scene):
    header = None
    back_btn = None

    select_btn = None
    name_text = None

    random_diff_btn = None
    easy_btn = None
    normal_btn = None
    hard_btn = None
    difficulty = -1

    random_pen_data = None
    pen_images = []
    visible_pen_images = []
    left_btn, right_btn = None, None

    center_pos = None
    pen_index = 0

    def start(self, screen):
        if not self.already_loaded:
            AIData.load_all_ais()

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
            self.random_diff_btn = ToggleButton(pygame.Rect(width * 1 / 5 - 50, 100, 100, 30), "Random", btn_options)
            self.easy_btn = ToggleButton(pygame.Rect(width * 2 / 5 - 50, 100, 100, 30), "Easy", btn_options)
            self.normal_btn = ToggleButton(pygame.Rect(width * 3 / 5 - 50, 100, 100, 30), "Normal", btn_options)
            self.hard_btn = ToggleButton(pygame.Rect(width * 4 / 5 - 50, 100, 100, 30), "Hard", btn_options)
            toggle_group = [self.random_diff_btn, self.easy_btn, self.normal_btn, self.hard_btn]
            for elt in toggle_group:
                elt.set_group(toggle_group)
            self.easy_btn.toggle()

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
                    self.random_diff_btn, self.easy_btn, self.normal_btn, self.hard_btn):
            elt.update(event)

        if self.select_btn.clicked:
            PenData.current_enemy_pen = \
                random.choice(PenData.all_pens) if self.pen_index == 0 else \
                PenData.all_pens[self.pen_index - 1]

            PenData.current_enemy_difficulty = \
                AIDifficulty.EASY if self.easy_btn.toggled else \
                AIDifficulty.NORMAL if self.normal_btn.toggled else \
                AIDifficulty.HARD if self.hard_btn.toggled else \
                random.choice(list(AIDifficulty))

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
                    self.easy_btn, self.normal_btn, self.hard_btn, self.random_diff_btn):
            elt.draw(screen)

        for img in self.visible_pen_images:
            img.draw(screen)
