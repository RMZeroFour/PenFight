import pygame
from scene import Scene
from gui import (Label, Button, Options)


class AboutScene(Scene):
    back_btn = None
    about_labels = []
    version_label = None

    def start(self, screen):
        if not self.already_loaded:
            self.back_btn = Button(pygame.rect.Rect(10, 10, 60, 40), "Back", {
                Options.BORDER_WIDTH: 0,
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
                Options.FONT: pygame.font.SysFont("Comic Sans MS", 15)
            })

            text_options = {
                Options.BACKGROUND: (82, 173, 200),
                Options.FOREGROUND: (20, 61, 89),
                Options.BORDER_WIDTH: 0
            }

            about_text = ["This game was made by Ritobroto Mukherjee and",
                         "Shivam Gupta (who has done absolutely nothing)",
                         "as practice for collaboration on a group project."]
            y_offset = 0
            for line in about_text:
                lbl = Label(pygame.Rect(10, 300 + y_offset * 30, screen.get_width() - 10, 30), line, text_options)
                self.about_labels.append(lbl)
                y_offset += 1

            version_text = "PenFight v1.0"
            self.version_label = Label(pygame.Rect(screen.get_width() / 2 - 25, screen.get_height() - 50, 50, 30),
                                       version_text, text_options)

            self.already_loaded = True

    def update(self, event):
        self.back_btn.update(event)

        if self.back_btn.clicked:
            Scene.pop_scene()

    def draw(self, screen):
        screen.fill((82, 173, 200))
        self.back_btn.draw(screen)
        for elt in self.about_labels + [self.version_label]:
            elt.draw(screen)
