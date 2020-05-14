# Import the needed libraries
import pygame

# Create a custom event to handle changing of scenes
SCENE_TRANSITION = pygame.USEREVENT + 1


# Base class for scenes
class Scene:
    # First time loading the scene
    already_loaded = False

    # Called once on transition
    def start(self, width, height):
        return

    # Called for every event
    def update(self, event):
        return

    # Called every frame
    def draw(self, screen):
        return

    # Used to fire the SCENE_TRANSITION event to change scenes based on index
    # I Should really have created a Finite State Machine, but this is fine for a small game like this :-P
    @staticmethod
    def change_scene(scene_id):
        event = pygame.event.Event(SCENE_TRANSITION, {"next_scene_id": scene_id})
        pygame.event.post(event)
