import pygame
from os import walk
from pygame.math import Vector2
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self, position, groups, path, colliders ) -> None:
        super().__init__(groups)
        self.import_assets(path)
        self.frame_index = 0
        self.fps = 8
        self.status = 'down_idle'
        self.sfx = pygame.mixer.Sound('sound/hit.mp3')

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = position)

        # Float based movement
        self.position = Vector2((self.rect.center))
        self.direction = Vector2()
        self.speed = 300

        # Coliisions
        self.hitbox = self.rect.inflate(-self.rect.width/2, -self.rect.height / 2)
        self.colliders = colliders
        self.mask = pygame.mask.from_surface(self.image)

        # Attack
        self.is_attacking = False

        # Health
        self.health = 3
        self.is_vulnerable = True
        self.inv_frames = None

    def import_assets(self, path):
        self.animations = {} # k:anim_status v: anim_frames
        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(folder[2], key=lambda x: int(x.split('.')[0])):
                    frame_path = folder[0].replace('\\', '/') + '/' + file_name #graphics/player/name/file_name.png
                    # print(frame_path)
                    frame_surf = pygame.image.load(frame_path).convert_alpha()
                    key = folder[0].split('\\')[1] 
                    self.animations[key].append(frame_surf)

    def move(self, delta):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.position.x += self.direction.x * self.speed * delta
        self.hitbox.centerx = round(self.position.x)
        self.rect.centerx = self.hitbox.centerx
        self.collide('horizontal')
        
        # Vertical movement
        self.position.y += self.direction.y * self.speed * delta
        self.hitbox.centery = round(self.position.y)
        self.rect.centery = self.hitbox.centery
        self.collide('vertical')

    def collide(self, direction):
        for sprite in self.colliders.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right
                    
                    self.rect.centerx = self.hitbox.centerx
                    self.position.x = self.hitbox.centerx
                
                elif direction == 'vertical':    
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                
                    self.rect.centery = self.hitbox.centery
                    self.position.y = self.hitbox.centery

    def deal_damage(self):
        
        if self.is_vulnerable:
            self.health -= 1
            self.is_vulnerable = False
            self.inv_frames = pygame.time.get_ticks()
            self.sfx.play()
    
    def die(self):
        if self.health <= 0:
            self.kill()

    def inv_timer(self):
        if not self.is_vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.inv_frames > 400:
                self.is_vulnerable = True

    def blink(self):
        if self.is_vulnerable: return
        if sin(pygame.time.get_ticks()) < 0:
            mask = pygame.mask.from_surface(self.image)
            white_surf = mask.to_surface()
            white_surf.set_colorkey((0,0,0))
            self.image = white_surf