import pygame
from pygame.math import Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, path, colliders) -> None:
        super().__init__(groups)
        self.image = pygame.Surface((100,100))
        self.image.fill('red')
        self.rect = self.image.get_rect(center = position)

        # Float based movement
        self.position = Vector2((self.rect.center))
        self.direction = Vector2()
        self.speed = 100

        # Coliisions
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        self.colliders = colliders

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0


        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, delta):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.position.x += self.direction.x * self.speed * delta
        self.hitbox.centerx = round(self.position.x)
        self.rect.centerx = self.hitbox.centerx
        #TODO: Horizontal position
        
        # Vertical movement
        self.position.y += self.direction.y * self.speed * delta
        self.hitbox.centery = round(self.position.y)
        self.rect.centery = self.hitbox.centery
        #TODO: Vertical position

    def update(self, delta):
        self.input()
        self.move(delta)
        