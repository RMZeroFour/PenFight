import pygame


# Class used for resource management
class Resources:
    # Dictionary to store all resources
    storage = {}

    # Store a resource with a key
    @staticmethod
    def add(key, resx):
        Resources.storage[key] = resx

    # Retrieve a resource by its key
    @staticmethod
    def get(key):
        return Resources.storage[key]

    # Check if a key exists
    @staticmethod
    def has(key):
        return key in Resources.storage

    # Used to load a sprite asset from file
    @staticmethod
    def load_sprite(filename):
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load(filename)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.topleft = (0, 0)
        return sprite
