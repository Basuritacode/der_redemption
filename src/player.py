import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups: _Group) -> None:
        super().__init__(*groups)