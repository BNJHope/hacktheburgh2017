#!/usr/bin/python

import logging
import math
import pygame

SHIP_WIDTH = 110
SHIP_HEIGHT = 110

GUN_WIDTH = 15
GUN_HEIGHT = 100

BULLET_WIDTH = 10
BULLET_HEIGHT = 10
BULLET_MOVEMENT = 10

ENEMY_WIDTH = 75
ENEMY_HEIGHT = 75
ENEMY_MOVEMENT = 110.0

class Entity():
    
    def __init__(self, identifier,  x, y, w, h, rot, log=False):

        self.COORDINATE_X = 0
        self.COORDINATE_Y = 1
        self.identifier = identifier

        self.x = x
        self.y = y
        self.width = w
        self.height = h

        self.update_position()

        self.rotation = rot
        if log:
            self.logger = logging.getLogger("world.{}".format(self.identifier))
            self.logger.setLevel(logging.INFO)
            self.logger.info("created entity")

    def move(self, x_delta, y_delta):
        self.x += x_delta
        self.y += y_delta
        self.update_position()

    def rotate(self, degrees):
        self.rotation += degrees
        self.rotate_rect_points()

    def collides_with(self, other_entity):
        return self.rect.colliderect(other_entity.rect)
       
    def get_area(self):
        return self.width * self.height 

    def update_position(self):
        self.update_rect()
        self.update_pointlist();

    def update_rect(self):
        rect = pygame.Rect(0, 0, self.width, self.height)
        rect.center = (self.x, self.y)

        self.rect = rect

    def update_pointlist(self):
        self.pointlist = [self.rect.topleft, self.rect.topright, self.rect.bottomright, self.rect.bottomleft]

    def rotate_point(self, point):
        rotation_angle = math.radians(self.rotation)

        s = math.sin(rotation_angle)
        c = math.cos(rotation_angle)

        point = list(point)

        point[self.COORDINATE_X] -= self.x
        point[self.COORDINATE_Y] -= self.y

        x_new = point[self.COORDINATE_X] * c - point[self.COORDINATE_Y] * s
        y_new = point[self.COORDINATE_X] * s + point[self.COORDINATE_Y] * c

        point[self.COORDINATE_X] = x_new + self.x
        point[self.COORDINATE_Y] = y_new + self.y

        return tuple(point)

    def rotate_rect_points(self):
        tl, tr, br, bl = self.pointlist

        tl = self.rotate_point(self.rect.topleft)
        tr = self.rotate_point(self.rect.topright)
        br = self.rotate_point(self.rect.bottomright)
        bl = self.rotate_point(self.rect.bottomleft)

        self.pointlist = [tl, tr, br, bl]


class Bullet(Entity):
    def __init__(self, x, y, dir):
        Entity.__init__(self, "bullet", x, y, BULLET_WIDTH, BULLET_HEIGHT, dir)

    def move(self):
        rotation_radians = math.radians(self.rotation)
        self.x -= BULLET_MOVEMENT*math.sin(rotation_radians)
        self.y -= BULLET_MOVEMENT*math.cos(rotation_radians)
        self.update_position()


class Gun(Entity):
    def __init__(self, ship):
        Entity.__init__(self, "gun", ship.x, ship.y, GUN_WIDTH, GUN_HEIGHT, 0)
        self.ammo = 25
        print("Gun built")

    def shoot(self):
        self.ammo -= 1

    def reload(self):
        self.ammo = 25


class Ship(Entity):
    def __init__(self, x, y, log=False):
        Entity.__init__(self, "ship", x, y, SHIP_WIDTH, SHIP_HEIGHT, 0, log)
        self.gun = Gun(self)

    def move(self, x_delta, y_delta, x_max, y_max):
        x = self.x + x_delta
        y = self.y + y_delta

        if not (x > x_max or x < 0 or y > y_max or y < 0):
            Entity.move(self, x_delta, y_delta)
            self.gun.move(x_delta, y_delta)
            self.gun.rotate_rect_points()

class Enemy(Entity):
    def __init__(self, x, y, target_x, target_y, rotation, surface):
        Entity.__init__(self, "enemy", x, y, ENEMY_WIDTH, ENEMY_HEIGHT, rotation)
        
        self.target_x = target_x
        self.target_y = target_y
        self.surface = surface

        dx, dy = (self.target_x - self.x, self.target_y - self.y)
        self.stepx = dx / ENEMY_MOVEMENT
        self.stepy = dy / ENEMY_MOVEMENT

    def move(self):
        Entity.move(self, self.stepx, self.stepy)


class World():
    def __init__(self, log=False):
        if log:
            self.logger = logging.getLogger("world")
            self.logger.setLevel(logging.INFO)  
            self.logger.info("created world")

        self.entities = []

    def register(self, entity):
        self.entities.append(entity)
        if self.logger:
            self.logger.info("registered entity: {}".format(entity.identifier))

class Engine():
    
    def main(self):
        logging.basicConfig()
        world = World(log=True)
        world.register(Ship(100, 100, log=True))

if __name__ == "__main__":
    engine = Engine()
    engine.main()
