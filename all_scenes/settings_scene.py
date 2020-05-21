import pygame
from scene import Scene
from gui import (Label, Textbox, Button, Options)
from settings import Settings
from account import Account


class SettingsScene(Scene):
    header = None
    back_btn = None

    volume_label, volume_box = None, None
    volume_value = 0

    def start(self, width, height):
        if not self.already_loaded:
            self.header = Label(pygame.rect.Rect(width / 2 - 50, 10, 150, 50), "Settings", options={
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

            label_options = {
                Options.BACKGROUND: (82, 173, 200),
                Options.FOREGROUND: (20, 61, 89),
                Options.BORDER_WIDTH: 0
            }

            self.volume_value = Account.current_account.settings.get(Settings.VOLUME)
            self.volume_label = Label(pygame.rect.Rect(width * 2 / 5, height * 2 / 5, 100, 30), "Volume", label_options)
            self.volume_box = Textbox(pygame.rect.Rect(width * 3 / 5, height * 2 / 5, 100, 30), str(self.volume_value))

            self.already_loaded = True

    def update(self, event):
        for elt in (self.volume_box, self.back_btn):
            elt.update(event)

        if self.back_btn.clicked:
            self.apply_changes()
            Scene.change_scene(4)

    def apply_changes(self):
        # Volume
        valid = SettingsScene.is_valid_number(self.volume_box.text)
        new_volume = int(self.volume_box.text) if valid else 0
        self.volume_value = new_volume if (new_volume >= 0) and (new_volume <= 100) else 0
        self.volume_box.set_text(str(self.volume_value))
        Account.current_account.settings.add(Settings.VOLUME, self.volume_value)

    @staticmethod
    def is_valid_number(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def draw(self, screen):
        screen.fill((82, 173, 200))

        for elt in (self.header, self.volume_label, self.volume_box, self.back_btn):
            elt.draw(screen)
