import pygame
from scene import Scene
from gui import (Label, Button, Textbox, Options)
from account import Account
from all_scenes import GameScene, GameOverScene
from game_code import GameResult


class ForfeitScene(Scene):
    confirm_text = None
    yes_btn = None
    no_btn = None
    underlay_screen = None

    # Create the various gui elements
    def start(self, screen):
        width = screen.get_width()
        height = screen.get_height()

        if not self.already_loaded:
            self.confirm_text = Label(pygame.rect.Rect(width / 2 - 200, height / 2 - 50, 400, 30),
                                      "Are you sure you want to forfeit the match?", {
                Options.BACKGROUND: (82, 173, 200),
                Options.FOREGROUND: (20, 61, 89),
                Options.BORDER_WIDTH: 0
            })
            self.yes_btn = Button(pygame.rect.Rect(width / 2 - 100, height / 2 + 50, 50, 40), "Yes", options={
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
                Options.BORDER_WIDTH: 0,
            })
            self.no_btn = Button(pygame.rect.Rect(width / 2 + 50, height / 2 + 50, 50, 40), "No", options={
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
                Options.BORDER_WIDTH: 0,
            })

        self.underlay_screen = screen.copy()
        self.already_loaded = True

    def update(self, event):
        for elt in (self.yes_btn, self.no_btn):
            elt.update(event)

        if self.yes_btn.clicked:
            state = GameResult.VictoryState.LOSE
            GameOverScene.result = GameResult(state)

            Scene.fire_event = False
            for i in range(0, 2):
                Scene.pop_scene()
            Scene.fire_event = True

            GameScene.game_over = True
            Scene.push_scene(10)

        if self.no_btn.clicked:
            Scene.pop_scene()

    # Clear the screen and draw the gui
    def draw(self, screen):
        screen.fill((82, 173, 200))
        screen.blit(self.underlay_screen, (0, 0))

        width = screen.get_width()
        height = screen.get_height()

        pygame.draw.rect(screen, (82, 173, 200),
                         pygame.rect.Rect(width * 1 / 5, height * 1 / 5, width * 3 / 5, height * 3 / 5))

        for elt in (self.confirm_text, self.yes_btn, self.no_btn):
            elt.draw(screen)
