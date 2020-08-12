import pygame
from game_code import GameResult
from account import Account
from scene import Scene
from gui import (Label, Button, Options)


class GameOverScene(Scene):

    result = None

    title = None
    win_state_text = None
    replay_btn = None
    main_menu_btn = None

    def start(self, screen):
        width, height = screen.get_width(), screen.get_height()

        if not self.already_loaded:

            self.title = Label(pygame.rect.Rect(width / 2 - 200, 10, 400, 30), "Game Over", options={
                    Options.BACKGROUND: (20, 61, 89),
                    Options.FOREGROUND: (244, 180, 26),
                    Options.BORDER_WIDTH: 0,
                })

            btn_options = {
                Options.BORDER_WIDTH: 0,
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
                Options.FONT: pygame.font.SysFont("Comic Sans MS", 20),
            }

            btn_rect = pygame.rect.Rect(width / 2 - 125, height * 3 / 5 - 50, 250, 30)
            self.replay_btn = Button(btn_rect, "Play again", btn_options)
            self.main_menu_btn = Button(btn_rect.copy().move(0, 75), "Go to main menu", btn_options)

            self.already_loaded = True

        self.recreate_victory_texts(width, height)

        Account.current_account.reward_money(GameOverScene.result.coins)
        if GameOverScene.result.state == GameResult.VictoryState.WIN:
            Account.current_account.add_win()
        elif GameOverScene.result.state == GameResult.VictoryState.LOSE:
            Account.current_account.add_loss()

    def recreate_victory_texts(self, w, h):
        coins = GameOverScene.result.coins
        text = f"You won the match! Received {coins} coins." if GameOverScene.result.state == GameResult.VictoryState.WIN else \
               "You lost the match!" if GameOverScene.result.state == GameResult.VictoryState.LOSE else \
               f"The match was a tie! Received {coins} coins."

        self.win_state_text = Label(pygame.rect.Rect(w / 2 - 300, 175, 600, 30), text, {
            Options.BACKGROUND: (82, 173, 200),
            Options.FOREGROUND: (20, 61, 89),
            Options.BORDER_WIDTH: 0,
        })

    def update(self, event):
        for btn in (self.replay_btn, self.main_menu_btn):
            btn.update(event)

        if self.replay_btn.clicked:
            Scene.fire_event = False
            for i in range(0, 2):
                Scene.pop_scene()
            Scene.fire_event = True
            Scene.pop_scene()

        elif self.main_menu_btn.clicked:
            Scene.fire_event = False
            for i in range(0, 3):
                Scene.pop_scene()
            Scene.fire_event = True
            Scene.pop_scene()

    # Clear the screen and draw the gui
    def draw(self, screen):
        screen.fill((82, 173, 200))

        self.title.draw(screen)

        for elt in (self.replay_btn, self.main_menu_btn, self.win_state_text):
            elt.draw(screen)
