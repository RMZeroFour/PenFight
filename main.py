# Import and initialize the pygame library
import pygame
pygame.init()

# Import the custom gui elements
import gui

# Set up the game window
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pygame Test")

# Create a demo label, button and textbox
hello_btn = gui.Button(pygame.rect.Rect(10, 100, 100, 50), "Hello", {
                gui.Options.BACKGROUND: (255, 0, 0),
                gui.Options.FOREGROUND: (0, 255, 0)
            })
gui_elements = [
    gui.Label(pygame.rect.Rect(10, 0, 200, 50), "Click this button"),
    gui.Label(pygame.rect.Rect(10, 50, 200, 50), "Type into this box"),
    hello_btn,
    gui.Textbox(pygame.rect.Rect(10, 200, 100, 50))
]

# Run until the window closes
finished = False
while not finished:

    # Check is the user clicks the window close button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

        # Update the gui elements
        for elt in gui_elements:
            elt.update(event)

        # Print hello if the button was pressed
        if hello_btn.clicked:
            print("hello")

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Draw the gui elements to the screen
    for elt in gui_elements:
        elt.draw(screen)

    # Display the graphics
    pygame.display.flip()

# Done! Time to quit
pygame.quit()