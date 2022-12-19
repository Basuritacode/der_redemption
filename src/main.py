import pygame, sys
from settings import *


class Game():
    def __init__(self): 
        ''' Basic Setup of pygame, includes the display and the clock'''
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('DRD2')
        self.clock = pygame.time.Clock()

    def terminate(self):
        ''' Terminates pygame execution and uses sys.exit to kill the whole program'''
        pygame.quit()
        sys.exit()
   
    def run(self): 
        ''' Contains the main game loop. 
            includes the event loop, 
            update functions and delta declaration
        '''
        while True:
            delta = self.clock.tick() / 100
            
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

            # Render
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()