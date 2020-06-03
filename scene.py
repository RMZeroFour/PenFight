# Import the needed libraries
import pygame

# Create a custom event to handle changing of scenes
SCENE_TRANSITION = pygame.USEREVENT + 1

# Base class for scenes
class Scene:

    # Maintain a stack of scenes
    scene_stack = []

    # First time loading the scene
    already_loaded = False

    # Called once on transition
    def start(self, screen):
        return

    # Called for every event
    def update(self, event):
        return

    # Called every frame
    def draw(self, screen):
        return

    # I Should really have created a Finite State Machine, but this is fine for a small game like this :-P

    # Used to fire the SCENE_TRANSITION event to push a scene onto the scene stack, that is, load the next scene
    @staticmethod
    def push_scene(next_scene_id):
        Scene.scene_stack.append(next_scene_id)
        event = pygame.event.Event(SCENE_TRANSITION)
        pygame.event.post(event)

    # Used to fire the SCENE_POP event to pop a scene from the scene stack, that is, return to the previous scene
    @staticmethod
    def pop_scene():
        Scene.scene_stack.pop()
        event = pygame.event.Event(SCENE_TRANSITION)
        pygame.event.post(event)
