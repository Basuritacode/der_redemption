import pygame
from entity import Entity
from pygame.math import Vector2

class Coffin(Entity):
    def __init__(self, position, groups, path, colliders, player) -> None:
        super().__init__(position, groups, path, colliders)
        #Reference to the player
        self.player = player
        self.agro_radius = 550
        self.walk_radius = 400
        self.attack_radius = 50

class Cactus(Entity):
    def __init__(self, position, groups, path, colliders, player) -> None:
        super().__init__(position, groups, path, colliders)
    
        self.player = player