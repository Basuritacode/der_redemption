import pygame
from pygame.math import Vector2

class Entity(pygame.sprite.Sprite):
    def __init__(self, position, groups, path, colliders ) -> None:
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
        self.hitbox = self.rect.inflate(-self.rect.width/2, -self.rect.height / 2)
        self.colliders = colliders

        # Attack
        self.is_attacking = False