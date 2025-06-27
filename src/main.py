import pygame
from config import WIDTH, HEIGHT, NUM_BOIDS, WINDOW_TITLE
from boid import Boid

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()
boids = [Boid() for _ in range(NUM_BOIDS)]

running = True
while running:
    screen.fill((10, 10, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for b in boids:
        b.update(boids)
        b.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
