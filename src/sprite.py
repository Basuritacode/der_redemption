import pygame
from pygame.math import Vector2

class Sprite(pygame.sprite.Sprite):
    def __init__(self, position, surface, *groups) -> None:
        super().__init__(*groups)
        self.image = surface
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0, -self.rect.height/3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, surface, direction, *groups) -> None:
        super().__init__(*groups)
        self.image = surface
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=position)
        self.sfx = pygame.mixer.Sound('sound/bullet.wav')
        self.sfx.play()

        self.position = Vector2(self.rect.center)
        self.direction = direction
        self.speed = 500

    def update(self, delta):
        self.position += self.direction * self.speed * delta
        self.rect.center = (round(self.position.x), round(self.position.y))
        