import pygame, sys
from settings import *
from player import Player
from sprite import Sprite, Bullet
from pygame.math import Vector2
from pytmx.util_pygame import load_pygame

class AllSprites(pygame.sprite.Group): #Camera Class: Centered to the player
    ''' The player keeps at the center of the screen
    all the other objects get offsetted relative to the player
    and move to the oposite direction of the player'''
    def __init__(self):
        super().__init__()
        self.offset = Vector2()
        self.display_surface = pygame.display.get_surface()
        self.background = pygame.image.load('graphics/other/background.png').convert()

    def my_draw(self, player: Player):
        # Move Camera Offset
        self.offset.x = player.rect.centerx - WINDOW_WIDTH/2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT/2

        # Display Background
        self.display_surface.blit(self.background, -self.offset)

        # All the sprites offseted
        for sprite in sorted(self.sprites(), key= lambda x: x.rect.centery):
            offset_rect = sprite.image.get_rect(center= sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

class Game():
    def __init__(self): 
        ''' Basic Setup of pygame, includes the display and the clock'''
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('DRD2')
        self.clock = pygame.time.Clock()
        self.bullet_surf = pygame.image.load('graphics/other/particle.png').convert_alpha()

        # Groups
        self.all_sprites = AllSprites()
        self.obstacles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.setup()
    
    def spawn_bullet(self, position, direction):
        Bullet(position, self.bullet_surf ,direction, [self.all_sprites, self.bullets])

    def setup(self):
        tmx_map = load_pygame('data/map.tmx')
        for x,y,surf in tmx_map.get_layer_by_name('Fence').tiles():
            Sprite((x*64, y*64), surf, [self.all_sprites, self.obstacles])

        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.image == None: continue
            Sprite((obj.x,obj.y), obj.image, [self.all_sprites, self.obstacles])

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player(
                    position = (obj.x,obj.y), 
                    groups = self.all_sprites, 
                    path = PATHS['player'], 
                    colliders = self.obstacles,
                    spawn_bullet = self.spawn_bullet
                )

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
            self.all_sprites.my_draw(self.player)

            # Render
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()