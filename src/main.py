import pygame, sys
from settings import *
from player import Player


class Game():
    def __init__(self): 
        ''' Basic Setup of pygame, includes the display and the clock'''
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('DRD2')
        self.clock = pygame.time.Clock()

        # Groups
        self.all_sprites = pygame.sprite.Group()

        self.setup()

    def setup(self):
        Player((100,100), self.all_sprites, PATHS['player'], None)

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
            delta = self.clock.tick() / 1000
            
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

            # Update gruops
            self.all_sprites.update(delta)

            # Draw groups
            self.display.fill('black')
            self.all_sprites.draw(self.display)

            # Render
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()