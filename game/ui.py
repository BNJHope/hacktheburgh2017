import pygame
import math
from main import *

def move_poly(polygon, x, y):
    for points in polygon:
        points[0] += x
        points[1] += y

    return polygon

def draw_ship(screen, ship):
    ship_body = pygame.Rect(0, 0, ship.width, ship.height)
    ship_body.center = (ship.x_pos, ship.y_pos)

    gun = ship.gun
    gun_body = pygame.Rect(0, 0, gun.width, gun.height)
    gun_body.center = (gun.x_pos, gun.y_pos)

    pygame.draw.rect(screen, GREEN, ship_body)
    pygame.draw.rect(screen, RED, gun_body)


running = True

size = (1600, 900)
GREEN = (0, 255,0)
WHITE = (0,0,0)
RED = (255, 0, 0)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Game.hs")

SHIP = Ship(800, 850)
MOVEMENT_CONSTANT = 50

print(pygame.QUIT)

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.dict["key"] == pygame.K_LEFT:
                SHIP.move(-MOVEMENT_CONSTANT, 0)
            if event.dict["key"] == pygame.K_RIGHT:
                SHIP.move(MOVEMENT_CONSTANT,0)
            if event.dict["key"] == pygame.K_UP:
                SHIP.move(0, -MOVEMENT_CONSTANT)
            if event.dict["key"] == pygame.K_DOWN:
                SHIP.move(0, MOVEMENT_CONSTANT)

    draw_ship(screen, SHIP)

    pygame.display.flip()

pygame.quit()