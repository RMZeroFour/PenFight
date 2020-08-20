import pygame
from scene import Scene
from gui import (Label, Button, Image, Options)
from resources import Resources
from account import Account
from game_code import PenData


class PenSelectScene(Scene):
    header = None
    back_btn = None

    select_btn = None
    purchase_btn = None

    name_text = None
    density_text = None
    restitution_text = None
    description_lines = []

    coins_image = None
    coins_text = None

    pen_images = []
    visible_pen_images = []
    left_btn, right_btn = None, None

    center_pos = None
    pen_index = 0

    def start(self, screen):
        if not self.already_loaded:
            PenData.load_all_pens(Resources.get("all_pens"))

            width = screen.get_width()
            height = screen.get_height()

            self.back_btn = Button(pygame.Rect(10, 10, 60, 40), "Back", {
                Options.BORDER_WIDTH: 0,
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
                Options.FONT: pygame.font.SysFont("Comic Sans MS", 15)
            })

            label_options = {
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.BORDER_WIDTH: 0,
            }
            self.header = Label(pygame.Rect(width / 2 - 200, 10, 400, 30), "Select your weapon!", label_options)
            self.coins_text = Label(pygame.Rect(width - 110, height - 55, 100, 40), "0", label_options)

            label_options = {
                Options.BACKGROUND: (82, 173, 200),
                Options.FOREGROUND: (20, 61, 89),
                Options.BORDER_WIDTH: 0,
                Options.FONT: pygame.font.SysFont("Comic Sans MS", 18)
            }
            self.density_text = Label(pygame.Rect(width / 5, 110, 100, 20), "Density: ", label_options)
            self.restitution_text = Label(pygame.Rect(width / 5, 130, 100, 20), "Restitution: ", label_options)

            self.name_text = Label(pygame.Rect(width / 2 - 45, height - 125, 90, 50), "", label_options)
            self.description_lines = [Label(pygame.Rect(width * 2 / 3, 100 + i * 25, 100, 20), "", label_options)
                                      for i in range(0, 3)]

            self.coins_image = Image(pygame.Rect(width - 175, height - 60, 50, 50), Resources.get("coin"), {
                Options.BACKGROUND: (82, 173, 200)
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
            self.purchase_btn = Button(pygame.Rect(width / 2 - 125, height - 75, 250, 40), "", btn_options)

            self.center_pos = pygame.Rect(width / 2 - 50, height / 2 - 50, 100, 100)
            for pen in PenData.all_pens:
                self.pen_images.append(Image(self.center_pos, Resources.get(pen.image_file), {
                    Options.BACKGROUND: (82, 173, 200)
                }))

            self.already_loaded = True

        self.reposition_images()
        self.update_shop_data()
        self.reset_coin_text()

    def update(self, event):
        for elt in (self.back_btn, self.left_btn, self.right_btn):
            elt.update(event)

        cur_pen = PenData.all_pens[self.pen_index]
        if cur_pen.name in Account.current_account.pens:
            self.select_btn.update(event)
            if self.select_btn.clicked:
                PenData.current_pen = cur_pen
                Scene.push_scene(6)
        else:
            self.purchase_btn.set_enabled(Account.current_account.money >= cur_pen.cost)
            self.purchase_btn.update(event)
            if self.purchase_btn.clicked:
                Account.current_account.purchase_pen(cur_pen)
                self.reset_coin_text()

        if self.back_btn.clicked:
            Scene.pop_scene()

        if self.left_btn.clicked or self.right_btn.clicked:
            if self.left_btn.clicked:
                self.pen_index -= 1
                self.reposition_images()
            elif self.right_btn.clicked:
                self.pen_index += 1
                self.reposition_images()
            self.update_shop_data()

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

    def reset_coin_text(self):
        self.coins_text.text = str(Account.current_account.money)
        self.coins_text.recreate()

    def update_shop_data(self):
        cur_pen = PenData.all_pens[self.pen_index]

        self.name_text.text = cur_pen.name
        self.name_text.recreate()

        self.density_text.text = f"Density: {cur_pen.density}"
        self.density_text.recreate()

        self.restitution_text.text = f"Restitution: {cur_pen.restitution}"
        self.restitution_text.recreate()

        line_index = 0
        for line in cur_pen.description:
            self.description_lines[line_index].text = line
            self.description_lines[line_index].recreate()
            line_index += 1

        if cur_pen.name not in Account.current_account.pens:
            self.purchase_btn.text = f"Purchase for {cur_pen.cost}"
            self.purchase_btn.recreate()

    def draw(self, screen):
        screen.fill((82, 173, 200))

        for elt in (self.header, self.back_btn, self.left_btn, self.right_btn, self.name_text,
                    self.coins_image, self.coins_text, self.density_text, self.restitution_text):
            elt.draw(screen)

        for line in self.description_lines:
            line.draw(screen)

        if PenData.all_pens[self.pen_index].name in Account.current_account.pens:
            self.select_btn.draw(screen)
        else:
            self.purchase_btn.draw(screen)

        for img in self.visible_pen_images:
            img.draw(screen)
