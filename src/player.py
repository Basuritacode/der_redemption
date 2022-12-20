import pygame
from pygame.math import Vector2
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, path, colliders) -> None:
        super().__init__(groups)
        self.import_assets(path)
        self.frame_index = 0
        self.status = 'down'

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = position)

        # Float based movement
        self.position = Vector2((self.rect.center))
        self.direction = Vector2()
        self.speed = 300

        # Coliisions
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        self.colliders = colliders

        # Attack
        self.is_attacking = False

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

    def get_status(self):
        # Idle
        if self.direction.magnitude() == 0: 
            self.status = self.status.split('_')[0] + '_idle'
        # Attacking
        if self.is_attacking:
            self.status = self.status.split('_')[0] + '_attack'
        
    def animate(self, delta):
        current_animation = self.animations[self.status] 
        self.frame_index += 8 * delta
        if self.frame_index >= len(current_animation):
            self.frame_index = 0 
            self.is_attacking = False
    
        self.image = current_animation[int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()
        
        if self.is_attacking: return

        # Movement
        if keys[pygame.K_UP]:
            self.status = 'up'
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.status = 'down'
            self.direction.y = 1
        else:
            self.direction.y = 0
        
        if keys[pygame.K_LEFT]:
            self.status = 'left'
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.status = 'right'
            self.direction.x = 1
        else:
            self.direction.x = 0

        # Attack
        if keys[pygame.K_SPACE]:
            self.is_attacking = True
            self.direction = Vector2()
            self.frame_index = 0

    def move(self, delta):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.position.x += self.direction.x * self.speed * delta
        self.hitbox.centerx = round(self.position.x)
        self.rect.centerx = self.hitbox.centerx
        #TODO: Horizontal colliition
        
        # Vertical movement
        self.position.y += self.direction.y * self.speed * delta
        self.hitbox.centery = round(self.position.y)
        self.rect.centery = self.hitbox.centery
        #TODO: Vertical collition

        # 

    def update(self, delta):
        self.input()
        self.get_status()
        self.move(delta)
        self.animate(delta)
        