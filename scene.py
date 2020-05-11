# Import the needed libraries
import pygame
import gui

# Create a custom event to handle changing of scenes
SCENE_TRANSITION = pygame.USEREVENT + 1

# Base class for scenes
class Scene:
	# Called for every event
	def update(self, event):
		return
	# Called every frame
	def render(self, screen):
		return

	# Used to fire the SCENE_TRANSITION event to change scenes based on index
	# I Should really have created a Finite State Machine, but this is fine for a small game like this :-P
	def change_scene(self, scene_id):
		event = pygame.event.Event(SCENE_TRANSITION, { "next_scene_id" : scene_id })
		pygame.event.post(event)

# Dummy scene with cyan background
class TestScene1(Scene):
	
	btn = gui.Button(pygame.rect.Rect(20, 20, 70, 40), "Goto 2")
	title = gui.Label(pygame.rect.Rect(225, 20, 400, 50), "Python PenFight!", options = { 
		gui.Options.FONT: pygame.font.SysFont("Comic Sans MS", 40, bold=True, italic=False)
	})

	def update(self, event):
		self.btn.update(event)
		
		if self.btn.clicked:
			self.change_scene(1)

	def draw(self, screen):
		screen.fill((0, 255, 255))
		self.btn.draw(screen)
		self.title.draw(screen)

# Dummy scene with magenta background
class TestScene2(Scene):
	
	btn = gui.Button(pygame.rect.Rect(20, 20, 70, 40), "Goto 3")

	def update(self, event):
		self.btn.update(event)
		
		if self.btn.clicked:
			self.change_scene(2)

	def draw(self, screen):
		screen.fill((255, 0, 255))
		self.btn.draw(screen)

# Dummy scene with yellow background
class TestScene3(Scene):
	
	btn = gui.Button(pygame.rect.Rect(20, 20, 70, 40), "Goto 1")

	def update(self, event):
		self.btn.update(event)
		
		if self.btn.clicked:
			self.change_scene(0)

	def draw(self, screen):
		screen.fill((255, 255, 0))
		self.btn.draw(screen)