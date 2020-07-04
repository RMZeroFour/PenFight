import pygame
from scene import Scene
from gui import (Label, Button, Textbox, Options)
from account import Account

class CreateAccountScene(Scene):
    header = None
    name_box = None
    create_btn = None
    back_btn = None

    # Create the various gui elements
    def start(self, screen):
        width = screen.get_width()
        height = screen.get_height()

        if self.already_loaded:
            self.name_box.set_text("")

        else:
            self.header = Label(pygame.rect.Rect(width / 2 - 200, 10, 400, 30), "Add new account", options={
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.BORDER_WIDTH: 0,
            })
            self.name_box = Textbox(pygame.rect.Rect(width/2 - 200, height/2 - 50, 400, 30), "", options={
                Options.BORDER_WIDTH: 0,
            })
            self.create_btn = Button(pygame.rect.Rect(width / 2 - 100, height / 2 + 50, 200, 30), "Create", options={
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
                Options.BORDER_WIDTH: 0,
            })
            self.back_btn = Button(pygame.rect.Rect(10, 10, 60, 40), "Back", {
                Options.BORDER_WIDTH: 0,
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
                Options.FONT: pygame.font.SysFont("Comic Sans MS", 15)
            })

            self.already_loaded = True

    # Check the buttons and switch to corresponding scenes when clicked
    def update(self, event):
        for elt in (self.name_box, self.create_btn, self.back_btn):
            elt.update(event)

        self.create_btn.set_enabled(len(self.name_box.text) > 0)
        if self.create_btn.clicked:
            new_account = Account(self.name_box.text)
            Account.save_to_file(new_account)
            Scene.push_scene(1)

        if self.back_btn.clicked:
            Scene.push_scene(1)

    # Clear the screen and draw the gui
    def draw(self, screen):
        screen.fill((82, 173, 200))

        for elt in (self.header, self.name_box, self.create_btn, self.back_btn):
            elt.draw(screen)
