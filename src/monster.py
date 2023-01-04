import pygame
from entity import Entity
from pygame.math import Vector2

class Monster:
    def get_player_distance_dir(self):
        enemy_pos = Vector2(self.rect.center)
        player_pos = Vector2(self.player.rect.center)
        distance = (player_pos - enemy_pos).magnitude()
        if distance != 0 :
            direction = (player_pos - enemy_pos).normalize()
        else:
            direction = Vector2()

        return (distance, direction)    

    def walk_to_player(self):
        distance, direction = self.get_player_distance_dir()
        if self.attack_radius < distance < self.walk_radius:
            self.direction = direction
            self.status = self.status.split('_')[0]
            self.fps = 25
        else: 
            self.direction = Vector2()
            
    def face_player(self):
        distance, direction = self.get_player_distance_dir()
        if distance < self.agro_radius:
            if -0.5 < direction.y < 0.5:
                if direction.x < 0: # facing left
                    self.status = 'left_idle'
                else:
                    self.status = 'right_idle'
            else:
                if direction.y < 0: # Facing up
                    self.status = 'up_idle'
                else:
                    self.status = 'down_idle'
        self.fps = 8


class Coffin(Entity, Monster):
    def __init__(self, position, groups, path, colliders, player) -> None:
        super().__init__(position, groups, path, colliders)
        self.speed = 150
       
        #Reference to the player
        self.player = player
        self.agro_radius = 550
        self.walk_radius = 400
        self.attack_radius = 50

    def attack(self):
        distance = self.get_player_distance_dir()[0]
        if distance <= self.attack_radius and not self.is_attacking:
            self.is_attacking = True
            self.frame_index = 0

        if self.is_attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def animate(self, delta):
            current_animation = self.animations[self.status] 
            self.frame_index += self.fps * delta

            # Trigger the deal_damage function
            if int(self.frame_index) == 4 and self.is_attacking:
                if self.get_player_distance_dir()[0] < self.attack_radius:
                    self.player.deal_damage()

            if self.frame_index >= len(current_animation):
                self.frame_index = 0 
                if self.is_attacking: self.is_attacking = False
        
            self.image = current_animation[int(self.frame_index)]
            self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta) -> None:
        self.face_player()
        self.walk_to_player()
        self.move(delta)
        self.attack()
        self.animate(delta)
        self.blink()
        self.inv_timer()
        self.die()



class Cactus(Entity, Monster):
    def __init__(self, position, groups, path, colliders, player, spawn_bullet) -> None:
        super().__init__(position, groups, path, colliders)
        self.speed = 75
       
       # Reference to the player
        self.player = player
        self.agro_radius = 600
        self.walk_radius = 500
        self.attack_radius = 350

        self.bullet_shot = False
        self.spawn_bullet = spawn_bullet

    def attack(self):
        distance = self.get_player_distance_dir()[0]
        if distance <= self.attack_radius and not self.is_attacking:
            self.is_attacking = True
            self.frame_index = 0
            self.bullet_shot = False

        if self.is_attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def animate(self, delta):
            current_animation = self.animations[self.status] 
            self.frame_index += self.fps * delta

            # Shoot in the correct frame
            if int(self.frame_index) == 6 and self.is_attacking and not self.bullet_shot:
                direction = self.get_player_distance_dir()[1]
                bullet_offset = self.rect.center + direction * 90
                self.spawn_bullet(bullet_offset, direction)
                self.bullet_shot = True

            if self.frame_index >= len(current_animation):
                self.frame_index = 0 
                self.is_attacking = False
        
            self.mask = pygame.mask.from_surface(self.image)
            self.image = current_animation[int(self.frame_index)]

    def update(self, delta) -> None:
        self.face_player()
        self.walk_to_player()
        self.move(delta)
        self.attack()
        self.animate(delta)
        self.blink()
        self.inv_timer()
        self.die()
