import pygame
import random
import math
from config import WIDTH, HEIGHT, MAX_SPEED, NEIGHBOR_RADIUS, MAX_FORCE, BOID_FRICTION, WANDER_STRENGTH, COHESION_FACTOR, ALIGNMENT_FACTOR, SEPARATION_FACTOR

class Boid:
    def __init__(self):
        self.pos = pygame.Vector2(random.uniform(50, WIDTH-50), random.uniform(50, HEIGHT-50))
        angle = random.uniform(0, 2 * math.pi)
        self.vel = pygame.Vector2(math.cos(angle), math.sin(angle)) * random.uniform(1, 2)
        self.acc = pygame.Vector2()

    def flock(self, boids):
        separation = pygame.Vector2()
        alignment = pygame.Vector2()
        cohesion = pygame.Vector2()
        total = 0
        
        for other in boids:
            if other is self:
                continue
                
            distance = self.pos.distance_to(other.pos)
            if distance < NEIGHBOR_RADIUS and distance > 0:
                # SEPARATION
                if distance < NEIGHBOR_RADIUS / 2:
                    diff = self.pos - other.pos
                    if diff.length() > 0:
                        diff = diff.normalize()
                        diff /= distance
                        separation += diff
                
                # ALIGNEMENT
                alignment += other.vel
                
                # COHESION
                cohesion += other.pos
                total += 1
        
        if total > 0:
            # SEPARATION
            if separation.length() > 0:
                separation = separation.normalize() * MAX_SPEED
                separation = (separation - self.vel) * SEPARATION_FACTOR
                if separation.length() > MAX_FORCE:
                    separation = separation.normalize() * MAX_FORCE
            
            # ALIGNEMENT
            alignment /= total
            if alignment.length() > 0:
                alignment = alignment.normalize() * MAX_SPEED
                alignment = (alignment - self.vel) * ALIGNMENT_FACTOR
                if alignment.length() > MAX_FORCE:
                    alignment = alignment.normalize() * MAX_FORCE
            
            # COHESION
            cohesion /= total
            cohesion = cohesion - self.pos
            if cohesion.length() > 0:
                cohesion = cohesion.normalize() * MAX_SPEED
                cohesion = (cohesion - self.vel) * COHESION_FACTOR
                if cohesion.length() > MAX_FORCE:
                    cohesion = cohesion.normalize() * MAX_FORCE
            
            self.acc += separation + alignment + cohesion
        
        if random.random() < 0.1:
            wander_angle = random.uniform(0, 2 * math.pi)
            wander = pygame.Vector2(math.cos(wander_angle), math.sin(wander_angle))
            self.acc += wander * WANDER_STRENGTH

    def update(self, boids):
        self.acc = pygame.Vector2()
        
        self.flock(boids)
        self.avoid_walls()
        
        if self.acc.length() > MAX_FORCE:
            self.acc = self.acc.normalize() * MAX_FORCE
        
        self.vel += self.acc
        
        if self.vel.length() < 0.5:
            angle = random.uniform(0, 2 * math.pi)
            self.vel = pygame.Vector2(math.cos(angle), math.sin(angle)) * 0.5
        
        self.vel *= (1 - BOID_FRICTION)
        
        if self.vel.length() > MAX_SPEED:
            self.vel = self.vel.normalize() * MAX_SPEED

        self.pos += self.vel

    def avoid_walls(self):
        margin = 80
        turn_factor = 0.5
        
        if self.pos.x < margin:
            self.acc.x += turn_factor
        elif self.pos.x > WIDTH - margin:
            self.acc.x -= turn_factor
        
        if self.pos.y < margin:
            self.acc.y += turn_factor
        elif self.pos.y > HEIGHT - margin:
            self.acc.y -= turn_factor

    def draw(self, screen):
        if self.vel.length() > 0:
            angle = math.atan2(self.vel.y, self.vel.x)
        else:
            angle = 0
        
        size = 6
        
        # ENTITY BODY
        body_points = [
            (size * 1.5, 0),
            (-size, -size//2),
            (-size//2, 0),
            (-size, size//2)
        ]
        
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        
        rotated_body = []
        for x, y in body_points:
            rx = x * cos_a - y * sin_a + self.pos.x
            ry = x * sin_a + y * cos_a + self.pos.y
            rotated_body.append((rx, ry))

        pygame.draw.polygon(screen, (255, 255, 255), rotated_body)