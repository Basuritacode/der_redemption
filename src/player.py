import pygame
from pygame.math import Vector2
from entity import Entity

class Player(Entity):
    def __init__(self, position, groups, path, colliders, spawn_bullet) -> None:
        super().__init__(position, groups, path, colliders)

        self.bullet_shot = False
        self.spawn_bullet = spawn_bullet

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

        if int(self.frame_index) == 2 and self.is_attacking and not self.bullet_shot:
            bullet_offset = self.rect.center + self.bullet_dir * 70
            self.spawn_bullet(bullet_offset, self.bullet_dir)
            self.bullet_shot = True

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
            self.bullet_shot = False

            self.bullet_dir = Vector2()
            match self.status.split('_')[0]:
                case 'up': self.bullet_dir = Vector2(0,-1)
                case 'down': self.bullet_dir = Vector2(0,1)
                case 'left': self.bullet_dir = Vector2(-1,0)
                case 'right': self.bullet_dir = Vector2(1,0)

    def update(self, delta):
        self.input()
        self.get_status()
        self.move(delta)
        self.animate(delta)
        