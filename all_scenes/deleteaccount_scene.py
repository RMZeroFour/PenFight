import pygame
from scene import Scene
from gui import (Label, Button, Textbox, Options)
from account import Account

class DeleteAccountScene(Scene):
    header = None
    confirm_text = None
    yes_btn = None
    no_btn = None

    # Create the various gui elements
    def start(self, screen):
        width = screen.get_width()
        height = screen.get_height()

        if not self.already_loaded:
            self.header = Label(pygame.rect.Rect(width / 2 - 200, 10, 400, 30), "Delete an account", options={
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.BORDER_WIDTH: 0,
            })
            self.confirm_text = Label(pygame.rect.Rect(width / 2 - 200, height / 2 - 50, 400, 30), "", options={
                                          Options.BACKGROUND: (82, 173, 200),
                                          Options.FOREGROUND: (20, 61, 89),
                                          Options.BORDER_WIDTH: 0
                                      })
            self.yes_btn = Button(pygame.rect.Rect(width / 2 - 200, height / 2 + 50, 50, 30), "Yes", options={
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
                Options.BORDER_WIDTH: 0,
            })
            self.no_btn = Button(pygame.rect.Rect(width / 2 + 200, height / 2 + 50, 50, 30), "No", options={
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
                Options.BORDER_WIDTH: 0,
            })

            self.already_loaded = True

        self.confirm_text.set_text(f"Are you sure you want to delete account {Account.account_to_delete.name}?")

    def update(self, event):
        for elt in (self.yes_btn, self.no_btn):
            elt.update(event)

        if self.yes_btn.clicked:
            Account.delete_account(Account.account_to_delete)
            Account.account_to_delete = None
            Scene.push_scene(1)

        if self.no_btn.clicked:
            Scene.push_scene(1)

    # Clear the screen and draw the gui
    def draw(self, screen):
        screen.fill((82, 173, 200))

        for elt in (self.header, self.confirm_text, self.yes_btn, self.no_btn):
            elt.draw(screen)
