import pygame
from pygame.math import Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, path, collision_sprites) -> None:
        super().__init__(groups)
        self.image = pygame.Surface((100,100))
        self.image.fill('red')
        self.rect = self.image.get_rect(center = position)

        # Float based movement
        self.position = Vector2((self.rect.center))
        self.direction = Vector2()
        self.speed = 300

        # Coliisions
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        self.collision_sprites = collision_sprites

    def input(self):
        pass

    def move(self, delta):
        pass

    def update(self, delta):
        self.input()
        self.move(delta)
        