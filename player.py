import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.direction = pygame.Vector2(0, -1)  # Start facing upwards
        self.timer = 0

    def triangle(self):
        forward = self.direction
        right = forward.rotate(90)
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right * (self.radius / 1.5)
        c = self.position - forward * self.radius + right * (self.radius / 1.5)
        return [a, b, c]
        
    def draw(self, screen):
        pygame.draw.polygon(screen, 'white', self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        self.direction = pygame.Vector2(0, -1).rotate(-self.rotation)

    def move(self, dt):
        self.position += self.direction * PLAYER_SPEED * dt

    def shoot(self):
        if self.timer > 0:
            return None
        else:
            self.timer = PLAYER_SHOOT_COOLDOWN
            # Calculate the position of the shot (front of the player)
            shot_pos = self.position + self.direction * self.radius
            # Create a new shot with the player's current direction
            new_shot = Shot(shot_pos.x, shot_pos.y, self.direction)
            return new_shot

    def update(self, dt):
        self.timer -= dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(dt)
        if keys[pygame.K_d]:
            self.rotate(-dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            return self.shoot()
        return None