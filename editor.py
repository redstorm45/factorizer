import pygame
from pygame.locals import *


class Editor:
    def __init__(self):
        self.size = (500,500)

    def run(self):
        self.width = int(input("width:"))
        self.height = int(input("height:"))
        
        self.window = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Factorizer Editor")
        self.clock = pygame.time.Clock()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            #draw
            self.draw()

            #update
            self.clock.tick(10)

        pygame.quit()

    def draw(self):
        #background
        self.window.fill((50,50,50))

        #update screen
        pygame.display.flip()
