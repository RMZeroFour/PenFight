import pygame
from scene import (Scene, SCENE_TRANSITION)
from gui import (Label, Button, Options)


class AboutScene(Scene):
    back_btn = None
    about_labels = []

    def start(self, screen):
        if not self.already_loaded:
            self.back_btn = Button(pygame.rect.Rect(10, 10, 60, 40), "Back", {
                Options.BORDER_WIDTH: 0,
                Options.BACKGROUND: (20, 61, 89),
                Options.FOREGROUND: (244, 180, 26),
                Options.HOVERED_BACKGROUND: (10, 30, 45),
                Options.FONT: pygame.font.SysFont("Comic Sans MS", 15)
            })

            about_text = "This game was made by Ritobroto Mukherjee and\n" \
                         "Shivam Gupta (who has done absolutely nothing yet)\n" \
                         "as practice for collaboration."
            y_offset = 0
            for line in about_text.splitlines():
                self.about_labels.append(Label(pygame.rect.Rect(10, 200 + y_offset * 30, screen.get_width() - 10, 30),
                                               line,
                                               {
                                                   Options.BACKGROUND: (82, 173, 200),
                                                   Options.FOREGROUND: (20, 61, 89),
                                                   Options.BORDER_WIDTH: 0
                                               }))
                y_offset += 1

            self.already_loaded = True

    def update(self, event):
        self.back_btn.update(event)

        if self.back_btn.clicked:
            Scene.pop_scene()

    def draw(self, screen):
        screen.fill((82, 173, 200))
        self.back_btn.draw(screen)
        for elt in self.about_labels:
            elt.draw(screen)
