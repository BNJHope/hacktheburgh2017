import pygame
import math
from main import *
from random import randint
import random


pygame.mixer.init(44100, -16, 2, 2048)
pew = pygame.mixer.Sound("../sfx/pew.wav")
reload_sound = pygame.mixer.Sound("../sfx/reload.wav")
explosion = pygame.mixer.Sound("../sfx/exp2.wav")
noammo = pygame.mixer.Sound("../sfx/noammo.wav")
pygame.font.init()

def move_poly(polygon, x, y):
    for points in polygon:
        points[0] += x
        points[1] += y

    return polygon

def rot_center(image, center, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def draw_entity(screen, colour, entity):
    pygame.draw.polygon(screen, colour, entity.pointlist)

def draw_ship(screen, ship):
    screen.blit(ship_img, ship)
    draw_entity(screen, RED, ship.gun)

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
    
    if player_ship.x == x:
        x += 1

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

def rotate_point(x, y, point):
    rotation_angle = math.radians(self.rotation)

    s = math.sin(rotation_angle)
    c = math.cos(rotation_angle)

    point = list(point)

    point[0] -= x
    point[1] -= y

    x_new = point[0] * c - point[1] * s
    y_new = point[0] * s + point[1] * c

    point[0] = x_new + x
    point[1] = y_new + y

    return tuple(point)

def rotate_rect_points(rect):

    tl = rotate_point(rect.centerx, rect.centery, rect.topleft)
    tr = rotate_point(rect.centerx, rect.centery, rect.topright)
    br = rotate_point(rect.centerx, rect.centery, rect.bottomright)
    bl = rotate_point(rect.centerx, rect.centery, rect.bottomleft)

    return (tl, tr, br, bl)

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
NEXT_LIMIT_INC = 500

reloading = False
reload_timer = 20

clock = pygame.time.Clock()

def init():
    global ship_img
    global cannon
    global enemy1
    global enemy2
    global background
    global gameover_screen
    global start_screen
    global enemy_surfaces 
    global score
    global next_limit
    global MOVEMENT_CONSTANT
    global INVERSE_SPAWN_RATE
    global NEXT_LIMIT_INC
    global next_func

    MOVEMENT_CONSTANT = 25
    INVERSE_SPAWN_RATE = 40
    NEXT_LIMIT_INC = 500

    next_func = lambda *args: args

    score = 0
    next_limit = NEXT_LIMIT_INC

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

    ship_img = pygame.transform.scale(pygame.image.load("../imgs/ship.png"), (SHIP_WIDTH, SHIP_HEIGHT))
    cannon = pygame.transform.scale(pygame.image.load("../imgs/cannon.png"), (GUN_WIDTH, GUN_HEIGHT))
    enemy1 = pygame.transform.scale(pygame.image.load("../imgs/enemy.png"), (ENEMY_WIDTH, ENEMY_HEIGHT))
    enemy2 = pygame.transform.scale(pygame.image.load("../imgs/enemy2.png"), (ENEMY_WIDTH, ENEMY_HEIGHT))
    background = pygame.image.load("../imgs/background.png")
    gameover_screen = pygame.transform.scale(pygame.image.load("../imgs/gameover.png"), (1600, 900))
    start_screen = pygame.transform.scale(pygame.image.load("../imgs/start.png"), (1600, 900))

    enemy_surfaces = [enemy1, enemy2]

init()

screen.blit(start_screen, (0,0))
pygame.display.update()

while pygame.event.poll().type != pygame.KEYDOWN:
    pass



while running:
    if score >= next_limit:
        next_limit += NEXT_LIMIT_INC
        if not ENEMY_MOVEMENT - 10 <= 0:
            ENEMY_MOVEMENT -= 10.0
        if not INVERSE_SPAWN_RATE - 3 <= 0:
            INVERSE_SPAWN_RATE -= 3

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
                        explosion.play()
                        score += 200
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        break


        for enemy in enemies:
            enemy.move()
            if enemy.y < 0 or enemy.y > SCREEN_HEIGHT:
                enemies.remove(enemy)
            if enemy.collides_with(SHIP):
                explosion.play()
                enemies.remove(enemy)
                hp.width -= 60
                if hp.width <= 0:
                    gameover = True


       

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.dict["key"] == pygame.K_j:
                    next_func = lambda: SHIP.move(-MOVEMENT_CONSTANT, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
                if event.dict["key"] == pygame.K_l:
                    next_func = lambda: SHIP.move(MOVEMENT_CONSTANT,0, SCREEN_WIDTH, SCREEN_HEIGHT)
                if event.dict["key"] == pygame.K_i:
                    next_func = lambda: SHIP.move(0, -MOVEMENT_CONSTANT, SCREEN_WIDTH, SCREEN_HEIGHT)
                if event.dict["key"] == pygame.K_k:
                    next_func = lambda: SHIP.move(0, MOVEMENT_CONSTANT, SCREEN_WIDTH, SCREEN_HEIGHT)
                if event.dict["key"] == pygame.K_x:
                    if SHIP.gun.ammo <= 0:
                        noammo.play()
                        print("No ammo")
                    else:
                        new_bullet = Bullet(SHIP.gun.x, SHIP.gun.y, -SHIP.gun.rotation)
                        new_bullet2 = Bullet(SHIP.gun.x, SHIP.gun.y, -SHIP.gun.rotation + 180)
                        bullets.append(new_bullet)
                        bullets.append(new_bullet2)
                        SHIP.gun.shoot()
                        pew.play()
                if event.dict["key"] == pygame.K_z:
                    reloading = True
                    reload_sound.play()
                if event.dict["key"] == pygame.K_a:
                    next_func = lambda: SHIP.gun.rotate(-5)
                    cannon = rot_center(cannon, SHIP.rect.center, 5)

                if event.dict["key"] == pygame.K_d:
                    next_func = lambda: SHIP.gun.rotate(5)
                    cannon = rot_center(cannon, SHIP.rect.center, -5)

        next_func()
       

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

        pygame.display.update()

        clock.tick(60)

        score += 1

pygame.quit()
