import pygame
from scene import Scene
from gui import (Label, Button, Image, Options)
from resources import  Resources
from account import Account


class MainMenuScene(Scene):
    title = None

    play_btn = None
    stats_btn = None
    about_btn = None
    settings_btn = None
    back_btn = None

    # Create the various gui elements
    def start(self, screen):
        if self.already_loaded:
            return

        width = screen.get_width()
        height = screen.get_height()

        self.title = Label(pygame.rect.Rect(width / 2 - 200, height / 7, 400, 60), "Python Penfight!", options={
            Options.BACKGROUND: (20, 61, 89),
            Options.FOREGROUND: (244, 180, 26),
            Options.BORDER_WIDTH: 4,
            Options.FONT: pygame.font.SysFont("Comic Sans MS", 40, bold=True, italic=False)
        })

        btn_rect = pygame.rect.Rect(width / 2 - 125, height / 2 - 50, 250, 30)
        btn_options = {
            Options.BORDER_WIDTH: 0,
            Options.BACKGROUND: (20, 61, 89),
            Options.FOREGROUND: (244, 180, 26),
            Options.HOVERED_BACKGROUND: (10, 30, 45),
            Options.FONT: pygame.font.SysFont("Comic Sans MS", 25),
        }

        self.play_btn = Button(btn_rect, "Play", btn_options)
        self.stats_btn = Button(btn_rect.copy().move(0, 75), "Stats", btn_options)
        self.about_btn = Button(btn_rect.copy().move(0, 150), "About", btn_options)

        settings_gear_image = Resources.get("gear")
        settings_gear_rect = pygame.rect.Rect(width - 100, height - 100, 75, 75)
        self.settings_btn = Image(settings_gear_rect, settings_gear_image, {
            Options.BACKGROUND: (20, 61, 89),
            Options.HOVERED_BACKGROUND: (10, 30, 45)
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
        for btn in (self.play_btn, self.stats_btn, self.about_btn, self.back_btn, self.settings_btn):
            btn.update(event)

        # Goto single player pen select scene
        if self.play_btn.clicked:
            Scene.push_scene(5)

        # Goto the stats scene
        elif self.stats_btn.clicked:
            Scene.push_scene(11)

        # Goto the about scene
        elif self.about_btn.clicked:
            Scene.push_scene(12)

        elif self.settings_btn.clicked:
            Scene.push_scene(13)

        # Go back to account select scene
        elif self.back_btn.clicked:
            Account.save_to_file(Account.current_account)
            Scene.pop_scene()

    # Clear the screen and draw the gui
    def draw(self, screen):
        screen.fill((82, 173, 200))

        self.title.draw(screen)

        for btn in (self.play_btn, self.stats_btn, self.about_btn, self.back_btn, self.settings_btn):
            btn.draw(screen)
