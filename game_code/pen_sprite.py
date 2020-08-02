import pygame


class PenSprite(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.transformed_image = None
        self.rect = self.image.get_rect()
        self.center = self.rect.center

    def set_transform(self, location, rotation, scale=None):
        self.transformed_image = self.image.copy()

        if scale is not None:
            self.transformed_image = pygame.transform.scale(self.transformed_image, scale)
            self.rect = self.transformed_image.get_rect(center=self.rect.center)

        if rotation is not None:
            self.transformed_image = pygame.transform.rotate(self.transformed_image, rotation)
            self.rect = self.transformed_image.get_rect(center=self.rect.center)

        self.rect.center = location

    def draw(self, screen):
        screen.blit(self.transformed_image, self.rect)