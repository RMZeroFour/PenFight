import pygame
from scene import Scene
from gui import (Label, Button, Options)
from account import Account


class StatsScene(Scene):
    header = None
    back_btn = None

    statistics = []
    visible_stats = []
    up_btn, down_btn = None, None

    stat_index = 0
    first_offset = None

    all_metrics = {}

    @staticmethod
    def create_metrics():
        StatsScene.all_metrics = {
            "Total Wins": (lambda acc: acc.stats[Account.total_wins_key]),
            "Total Losses": (lambda acc: acc.stats[Account.total_losses_key]),
            "Total Money": (lambda acc: acc.stats[Account.total_money_key]),
            "Unlocked Pens": (lambda acc: acc.stats[Account.unlocked_pens_key]),
        }

    def start(self, screen):
        width = screen.get_width()
        height = screen.get_height()

        if not self.already_loaded:
            StatsScene.create_metrics()

            self.header = Label(pygame.rect.Rect(width / 2 - 200, 10, 400, 30), "Statistics", options={
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.BORDER_WIDTH: 0,
            })

            self.first_offset = pygame.rect.Rect(width / 2 - 125, 75, 250, 30)

            label_options = {
                Options.BACKGROUND: (82, 173, 200),
                Options.FOREGROUND: (20, 61, 89),
                Options.BORDER_WIDTH: 0
            }

            for metric in StatsScene.all_metrics.keys():
                text = f"{metric}: {StatsScene.all_metrics[metric](Account.current_account)}"
                stat_lbl = Label(pygame.rect.Rect(0, 0, 0, 0), text, label_options)
                self.statistics.append(stat_lbl)

            btn_options = {
                Options.BORDER_WIDTH: 0,
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
                Options.FONT: pygame.font.SysFont("Comic Sans MS", 15)
            }

            self.up_btn = Button(pygame.rect.Rect(width * 5 / 6, height * 1 / 5, 60, 40), "Up", btn_options)
            self.back_btn = Button(pygame.rect.Rect(10, 10, 60, 40), "Back", btn_options)
            self.down_btn = Button(pygame.rect.Rect(width * 5 / 6, height * 3 / 5, 60, 40), "Down", btn_options)

            self.already_loaded = True

        self.stat_index = 0
        self.reposition_stats()

    def update(self, event):
        for btn in (self.back_btn, self.up_btn, self.down_btn):
            btn.update(event)

        if self.back_btn.clicked:
            Scene.pop_scene()

        if self.up_btn.clicked:
            self.stat_index -= 1
            self.reposition_stats()
        elif self.down_btn.clicked:
            self.stat_index += 1
            self.reposition_stats()

    def reposition_stats(self):
        self.visible_stats.clear()

        offset = 0
        for stat in self.statistics[self.stat_index:self.stat_index + 10]:
            stat.rect = self.first_offset.copy().move(0, offset)
            stat.recreate()
            self.visible_stats.append(stat)
            offset += 50

        self.up_btn.set_enabled(self.stat_index > 0)
        self.down_btn.set_enabled(self.stat_index < len(self.statistics) - 1)

    def draw(self, screen):
        screen.fill((82, 173, 200))
        self.header.draw(screen)

        for stat in self.visible_stats:
            stat.draw(screen)

        width, height = screen.get_width(), screen.get_height()

        scroll_rect = pygame.rect.Rect(width * 5 / 6 + 100, height * 1 / 6, 10, height * 4 / 6)
        pygame.draw.rect(screen, (100, 100, 100), scroll_rect)

        height_diff = (height * 4 / 6) / len(self.statistics)
        scroll_rect.top = height * 1 / 6 + height_diff * self.stat_index
        scroll_rect.height = height_diff
        pygame.draw.rect(screen, (50, 50, 50), scroll_rect)

        for btn in (self.back_btn, self.up_btn, self.down_btn):
            btn.draw(screen)
