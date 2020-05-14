import pygame
from scene import Scene
from gui import (Label, Button, Options)
from account import Account
import math


class SelectAccountScene(Scene):
    header = None
    no_account_text = None

    account_btns = []
    visible_acc_btns = []
    delete_btns = {}
    up_btn, down_btn = None, None
    create_btn = None

    btn_index = 0
    first_offset = None

    # Create the various gui elements
    def start(self, width, height):
        if self.already_loaded:
            btn_options = {
                Options.BORDER_WIDTH: 0,
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
            }

            del_btn_options = {
                Options.BORDER_WIDTH: 0,
                Options.BACKGROUND: (200, 20, 40),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (150, 5, 20),
            }

            original_names = [btn.text for btn in self.account_btns]
            account_names = Account.get_account_names()

            for name in original_names:
                if name not in account_names:
                    btn_to_delete = self.account_btns[[idx for idx, btn in enumerate(self.account_btns) if btn.text == name][0]]
                    self.account_btns.remove(btn_to_delete)
                    self.delete_btns.pop(btn_to_delete)

            for name in account_names:
                if name not in original_names:
                    btn = Button(pygame.rect.Rect(0, 0, 0, 0), name, btn_options)
                    self.account_btns.append(btn)

                    del_btn = Button(pygame.rect.Rect(0, 0, 30, 30), "X", del_btn_options)
                    self.delete_btns[btn] = del_btn

            self.account_btns.sort(key=(lambda btn: btn.text))

        else:
            self.header = Label(pygame.rect.Rect(width / 2 - 200, 10, 400, 30), "Select account to load", options={
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.BORDER_WIDTH: 0,
            })
            self.no_account_text = Label(pygame.rect.Rect(width / 2 - 350, height/2, 550, 30),
                                         "No account created. Click the New button to make one.",
                                         options={
                                             Options.BACKGROUND: (82, 173, 200),
                                             Options.FOREGROUND: (20, 61, 89),
                                             Options.BORDER_WIDTH: 0,
                                         })

            self.first_offset = pygame.rect.Rect(width / 2 - 125, 75, 250, 30)

            btn_options = {
                Options.BORDER_WIDTH: 0,
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
            }

            del_btn_options = {
                Options.BORDER_WIDTH: 0,
                Options.BACKGROUND: (200, 20, 40),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (150, 5, 20),
            }

            account_names = Account.get_account_names()
            for name in account_names:
                btn = Button(pygame.rect.Rect(0, 0, 0, 0), name, btn_options)
                self.account_btns.append(btn)

                del_btn = Button(pygame.rect.Rect(0, 0, 30, 30), "X", del_btn_options)
                self.delete_btns[btn] = del_btn

            btn_options = {
                Options.BORDER_WIDTH: 0,
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
                Options.FONT: pygame.font.SysFont("Comic Sans MS", 15)
            }

            self.up_btn = Button(pygame.rect.Rect(width * 5 / 6, height * 1 / 5, 60, 40), "Up", btn_options)
            self.create_btn = Button(pygame.rect.Rect(width * 5 / 6, height * 2 / 5, 60, 40), "New", btn_options)
            self.down_btn = Button(pygame.rect.Rect(width * 5 / 6, height * 3 / 5, 60, 40), "Down", btn_options)

            self.already_loaded = True

        self.btn_index = 0
        self.reposition_buttons()

    # Check the buttons and switch to corresponding scenes when clicked
    def update(self, event):
        for btn in self.visible_acc_btns:
            btn.update(event)
            if btn.clicked:
                Account.current_account = Account.load_from_file(btn.text)
                Scene.change_scene(4)

            self.delete_btns[btn].update(event)
            if self.delete_btns[btn].clicked:
                Account.account_to_delete = Account.load_from_file(btn.text)
                Scene.change_scene(3)

        for btn in (self.create_btn, self.up_btn, self.down_btn):
            btn.update(event)

        if self.create_btn.clicked:
            Scene.change_scene(2)

        if self.up_btn.clicked:
            self.btn_index -= 1
            self.reposition_buttons()
        elif self.down_btn.clicked:
            self.btn_index += 1
            self.reposition_buttons()

    def reposition_buttons(self):
        self.visible_acc_btns.clear()

        offset = 0
        for btn in self.account_btns[self.btn_index:self.btn_index + 10]:
            btn.rect = self.first_offset.copy().move(0, offset)
            btn.recreate()
            self.visible_acc_btns.append(btn)

            offset += 50

            self.delete_btns[btn].rect.top = btn.rect.top
            self.delete_btns[btn].rect.left = btn.rect.right + 10
            self.delete_btns[btn].recreate()

        self.up_btn.set_enabled(self.btn_index > 0)
        self.down_btn.set_enabled(self.btn_index < len(self.account_btns) - 1)

    @staticmethod
    def near_mouse(point, max_dist):
        mouse_pos = pygame.mouse.get_pos()
        distance = ((point[0] - mouse_pos[0]) ** 2) + ((point[1] - mouse_pos[1]) ** 2)
        return distance < (max_dist ** 2)

    # Clear the screen and draw the gui
    def draw(self, screen):
        screen.fill((82, 173, 200))
        self.header.draw(screen)

        if len(self.account_btns) == 0:
            self.no_account_text.draw(screen)
        else:
            for btn in self.visible_acc_btns:
                btn.draw(screen)

                if self.near_mouse(self.delete_btns[btn].rect.center, 25):
                    self.delete_btns[btn].draw(screen)

            width, height = screen.get_width(), screen.get_height()

            scroll_rect = pygame.rect.Rect(width*5/6 + 100, height*1/6, 10, height*4/6)
            pygame.draw.rect(screen, (100, 100, 100), scroll_rect)

            height_diff = (height*4/6) / len(self.account_btns)
            scroll_rect.top = height*1/6 + height_diff * self.btn_index
            scroll_rect.height = height_diff
            pygame.draw.rect(screen, (50, 50, 50), scroll_rect)

        for btn in (self.create_btn, self.up_btn, self.down_btn):
            btn.draw(screen)
