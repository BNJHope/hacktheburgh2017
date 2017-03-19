import pygame
import math
from main import *
from random import randint
import random

def move_poly(polygon, x, y):
    for points in polygon:
        points[0] += x
        points[1] += y

    return polygon

def draw_entity(screen, colour, entity):
    pygame.draw.polygon(screen, colour, entity.pointlist)

def draw_ship(screen, ship):
    draw_entity(screen, GREEN, ship)
    draw_entity(screen, RED, ship.gun)
    # pygame.draw.rect(screen, RED, ship.gun.rect)

def draw_entities(screen, colour, entities):
    for entity in entities:
        draw_entity(screen, colour, entity)

running = True

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

def make_wall(x_min, x_max, y_min, y_max):
    return {
        "x_min": x_min,
        "x_max": x_max,
        "y_min": y_min,
        "y_max": y_max, 
    }

def create_enemy(wall, player_ship):
    x = randint(wall["x_min"], wall["x_max"])
    y = randint(wall["y_min"], wall["y_max"])

    return Enemy(x, y, player_ship.x, player_ship.y)

def generate_enemy(player_ship):
    walls = {
        "up": make_wall(0, SCREEN_WIDTH, 0, 0),
        "right": make_wall(SCREEN_WIDTH, SCREEN_WIDTH, 0, SCREEN_HEIGHT),
        "down": make_wall(0, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_HEIGHT),
        "left": make_wall(0, 0, 0, SCREEN_HEIGHT)
    }

    wall = random.choice(list(walls.items()))[1]

    return create_enemy(wall, player_ship)

size = (SCREEN_WIDTH, SCREEN_HEIGHT)
GREEN = (0, 255,0)
WHITE = (0,0,0)
RED = (255, 0, 0)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Game.hsii")

SHIP = Ship(800, 850)
MOVEMENT_CONSTANT = 10
INVERSE_SPAWN_RATE = 20

clock = pygame.time.Clock()

bullets = []
enemies = []

while running:
    screen.fill(WHITE)
    print(len(enemies))

    if randint(0, INVERSE_SPAWN_RATE) == 0:
        enemies.append(generate_enemy(SHIP))

    for bullet in bullets:
        bullet.move()
        if bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
            bullets.remove(bullet)
        else:        
            for enemy in enemies:
                if bullet.collides_with(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break


    for enemy in enemies:
        enemy.move()
        if enemy.y < 0 or enemy.y > SCREEN_HEIGHT:
            enemies.remove(enemy)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.dict["key"] == pygame.K_j:
                SHIP.move(-MOVEMENT_CONSTANT, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
            if event.dict["key"] == pygame.K_l:
                SHIP.move(MOVEMENT_CONSTANT,0, SCREEN_WIDTH, SCREEN_HEIGHT)
            if event.dict["key"] == pygame.K_i:
                SHIP.move(0, -MOVEMENT_CONSTANT, SCREEN_WIDTH, SCREEN_HEIGHT)
            if event.dict["key"] == pygame.K_k:
                SHIP.move(0, MOVEMENT_CONSTANT, SCREEN_WIDTH, SCREEN_HEIGHT)
            if event.dict["key"] == pygame.K_SPACE:
                new_bullet = Bullet(SHIP.gun.x, SHIP.gun.y, -SHIP.gun.rotation)
                bullets.append(new_bullet)
            if event.dict["key"] == pygame.K_a:
                SHIP.gun.rotate(-5)
            if event.dict["key"] == pygame.K_d:
                SHIP.gun.rotate(5)

    draw_ship(screen, SHIP)
    draw_entities(screen, RED, bullets)
    draw_entities(screen, RED, enemies)

    pygame.display.update()

    clock.tick(60)

pygame.quit()