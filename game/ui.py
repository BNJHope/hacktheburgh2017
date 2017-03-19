import pygame
import math
from main import *
from random import randint
import random

pygame.font.init()

enemy1 = pygame.transform.scale(pygame.image.load("../imgs/enemy.png"), (ENEMY_WIDTH, ENEMY_HEIGHT))
enemy2 = pygame.transform.scale(pygame.image.load("../imgs/enemy2.png"), (ENEMY_WIDTH, ENEMY_HEIGHT))
background = pygame.image.load("../imgs/background.png")
gameover_screen = pygame.image.load("../imgs/gameover.png")

enemy_surfaces = [enemy1, enemy2]


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

def draw_enemy(screen, enemy):
    enemy_surface = pygame.transform.rotate(enemy.surface, -enemy.rotation)
    screen.blit(enemy_surface, enemy)
    
def draw_enemies(screen, enemies):
    for enemy in enemies:
        draw_enemy(screen, enemy)
    
def draw_entities(screen, colour, entities):
    for entity in entities:
        draw_entity(screen, colour, entity)

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

    m = (player_ship.y - y) / (player_ship.x - x)
    # print(str(x) + " : " + str(y))

    theta = math.atan(m)
    angle = 90 + math.degrees(theta)

    if (x > player_ship.x):
        angle += 180

    return Enemy(x, y, player_ship.x, player_ship.y, angle, random.choice(enemy_surfaces))

def generate_enemy(player_ship):
    walls = {
        "up": make_wall(0, SCREEN_WIDTH, 0, 0),
        "right": make_wall(SCREEN_WIDTH, SCREEN_WIDTH, 0, SCREEN_HEIGHT),
        "down": make_wall(0, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_HEIGHT),
        "left": make_wall(0, 0, 0, SCREEN_HEIGHT)
    }

    wall = random.choice(list(walls.items()))[1]

    return create_enemy(wall, player_ship)


font = pygame.font.SysFont("monospace", 36)

size = (SCREEN_WIDTH, SCREEN_HEIGHT)
GREEN = (0, 255,0)
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
HP_WIDTH = 600
HP_HEIGHT = 50
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game.idr")

MOVEMENT_CONSTANT = 10
INVERSE_SPAWN_RATE = 40

reloading = False
reload_timer = 20

clock = pygame.time.Clock()

def init():
    global score
    score = 0

    global SHIP
    SHIP = Ship(800, 850)

    global running
    running = True

    global gameover
    gameover = False

    global bullets
    bullets = []

    global enemies
    enemies = []

    global hp
    hp = pygame.Rect(0, 0, HP_WIDTH, HP_HEIGHT)
    hp.center = (400, 50)


while pygame.event.poll().type != pygame.KEYDOWN:
    pass

init()

while running:

    if gameover:
        screen.blit(gameover_screen, (0,0))
        label = font.render("Final score: " + str(score), 1, WHITE)
        screen.blit(label, (700, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    running = False
            if event.type == pygame.KEYDOWN and event.dict["key"] == pygame.K_RETURN:
                init()
        pygame.display.update()

    else:
        screen.blit(background, (0,0))

        label = font.render("Score: " + str(score), 1, WHITE)
        screen.blit(label, (1200, 50))
        pygame.draw.rect(screen, RED, hp)

        if randint(0, INVERSE_SPAWN_RATE) == 0:
            enemies.append(generate_enemy(SHIP))

        for bullet in bullets:
            bullet.move()
            if bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
                bullets.remove(bullet)
            else:        
                for enemy in enemies:
                    if bullet.collides_with(enemy):
                        score += 200
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        break


        for enemy in enemies:
            enemy.move()
            if enemy.y < 0 or enemy.y > SCREEN_HEIGHT:
                enemies.remove(enemy)
            if enemy.collides_with(SHIP):
                enemies.remove(enemy)
                hp.width -= 60
                if hp.width < 0:
                    gameover = True


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
                if event.dict["key"] == pygame.K_x:
                    if SHIP.gun.ammo <= 0:
                        print("No ammo")
                    else:
                        new_bullet = Bullet(SHIP.gun.x, SHIP.gun.y, -SHIP.gun.rotation)
                        bullets.append(new_bullet)
                        SHIP.gun.shoot()
                if event.dict["key"] == pygame.K_z:
                    reloading = True
                if event.dict["key"] == pygame.K_a:
                    SHIP.gun.rotate(-5)
                if event.dict["key"] == pygame.K_d:
                    SHIP.gun.rotate(5)

        if reloading:
            reload_timer -= 1
            print("reloading")
            if reload_timer <= 0:
                SHIP.gun.reload()
                reload_timer = 20
                reloading = False

        draw_ship(screen, SHIP)
        draw_entities(screen, RED, bullets)
        draw_enemies(screen, enemies)
        #draw_entities(screen, RED, enemies)

        pygame.display.update()

        clock.tick(60)

        score += 1


pygame.quit()
