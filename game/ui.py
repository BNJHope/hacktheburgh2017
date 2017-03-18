import pygame
import math
from main import *

def move_poly(polygon, x, y):
    for points in polygon:
        points[0] += x
        points[1] += y

    return polygon

def draw_entity(screen, colour, entity):
    entity_body = pygame.Rect(0, 0, entity.width, entity.height)
    entity_body.center = (entity.x_pos, entity.y_pos)

    pygame.draw.rect(screen, colour, entity_body)

def draw_ship(screen, ship):
    pygame.draw.rect(screen, GREEN, ship.rect)
    pygame.draw.rect(screen, RED, ship.gun.rect)

def draw_bullets(screen, bullets):
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet.rect)

running = True

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

size = (SCREEN_WIDTH, SCREEN_HEIGHT)
GREEN = (0, 255,0)
WHITE = (0,0,0)
RED = (255, 0, 0)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Game.hs")

SHIP = Ship(800, 850)
MOVEMENT_CONSTANT = 50

clock = pygame.time.Clock()

bullets = []

while running:
    screen.fill(WHITE)

    for bullet in bullets:
        bullet.move()
        if bullet.rect.centery < 0 or bullet.rect.centery > SCREEN_HEIGHT:
            bullets.remove(bullet)

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
            if event.dict["key"] == pygame.K_SPACE:
                new_bullet = Bullet(SHIP.rect.centerx, SHIP.rect.centery, SHIP.rotation)
                bullets.append(new_bullet)
            if event.dict["key"] == pygame.K_a:
                SHIP.rotate(5)
            if event.dict["key"] == pygame.K_d:
                SHIP.rotate(-5)

    draw_ship(screen, SHIP)
    draw_bullets(screen, bullets)

    pygame.display.update()

    clock.tick(60)

pygame.quit()