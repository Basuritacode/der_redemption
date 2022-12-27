import pygame
from entity import Entity
from pygame.math import Vector2

class Coffin(Entity):
    def __init__(self, position, groups, path, colliders) -> None:
        super().__init__(position, groups, path, colliders)

class Cactus(Entity):
    def __init__(self, position, groups, path, colliders) -> None:
        super().__init__(position, groups, path, colliders)
        