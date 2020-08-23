import pygame
from scene import Scene
from resources import Resources
from gui import (Label, Image, Options)
from threading import Thread


class LoadingScene(Scene):
    loaded = False
    loading_text = None

    circle_image = None
    loading_circle = None
    circle_angle = 0

    def start(self, screen):
        if self.already_loaded:
            return

        # Spawn a new thread to load all resources
        Thread(target=self.load_assets).start()

        width = screen.get_width()
        height = screen.get_height()

        # Meanwhile create a label to show that the game is loading
        text_rect = pygame.rect.Rect(width / 2 - 100, height / 2 - 25, 200, 50)
        self.loading_text = Label(text_rect, "Loading...", {
            Options.BACKGROUND: (20, 61, 89),
            Options.FOREGROUND: (244, 180, 26),
            Options.BORDER_WIDTH: 0,
        })

        # Also create an image to display a rotate animation
        image_rect = pygame.rect.Rect(width / 2 - 50, height / 2 + 50, 75, 75)
        self.loading_circle = Image(image_rect, None, {
            Options.BACKGROUND: (82, 173, 200)
        })

        self.already_loaded = True

    def load_assets(self):
        # Load the circle loading animation
        Resources.add("loading", pygame.image.load("assets/loading.png"))
        self.circle_image = Resources.get("loading")

        # Load the settings gear icon
        Resources.add("gear", pygame.image.load("assets/gear.png"))

        # Load the close icon
        Resources.add("close", pygame.image.load("assets/close.png"))

        # Load the coin image
        Resources.add("coin", pygame.image.load("assets/coin.png"))

        # Load the random pen image
        Resources.add("random_pen", pygame.image.load("assets/random_pen.png"))

        # Load the pen data and images
        Resources.add("all_pens", Resources.load_text("assets/pens.json"))
        Resources.add("pencil", pygame.image.load("assets/pencil.png"))
        Resources.add("ball_pen", pygame.image.load("assets/ball_pen.png"))
        Resources.add("blue_gel_pen", pygame.image.load("assets/blue_gel_pen.png"))
        Resources.add("black_gel_pen", pygame.image.load("assets/black_gel_pen.png"))
        Resources.add("mech_pencil", pygame.image.load("assets/mech_pencil.png"))
        Resources.add("marker", pygame.image.load("assets/marker.png"))

        self.loaded = True

    def update(self, event):
        # If the circle loading image has been loaded then use it for the animation
        if (self.loading_circle.image is None) and (self.circle_image is not None):
            self.loading_circle.image = self.circle_image

    def draw(self, screen):
        screen.fill((82, 173, 200))

        # Wait if the loading has not finished
        if not self.loaded:
            self.loading_text.draw(screen)

            # Rotate the image to show a loading animation
            self.loading_circle.draw(screen)
            if self.loading_circle.image is not None:
                self.loading_circle.image = pygame.transform.rotate(self.circle_image, self.circle_angle)
                self.circle_angle = -(pygame.time.get_ticks() % 360)

        # If loading has finished, then go to account loading
        else:
            Scene.push_scene(1)
