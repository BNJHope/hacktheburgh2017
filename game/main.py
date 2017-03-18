#!/usr/bin/python

import logging
import math
import pygame

SHIP_WIDTH = 50
SHIP_HEIGHT = 50

GUN_WIDTH = 5
GUN_HEIGHT = 75

BULLET_WIDTH = 5
BULLET_HEIGHT = 5
BULLET_MOVEMENT = 10

class Entity():
    
    def __init__(self, identifier,  x, y, w, h, rot, log=False):

        self.COORDINATE_X = 0
        self.COORDINATE_Y = 1
       
        self.identifier = identifier
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.center = (x, y)
        self.rotation = rot
        if log:
            self.logger = logging.getLogger("world.{}".format(self.identifier))
            self.logger.setLevel(logging.INFO)
            self.logger.info("created entity")

    def move(self, x_delta, y_delta):
        rect = self.rect
        self.rect.center = (rect.centerx + x_delta, rect.centery + y_delta)

    def rotate(self, degrees):
        self.rotation += degrees
        self.rotate_rect_points()

    def collides_with(self, other_entity):
        print("yeah fuck me dude it collides")

    def compare_size(self, other_entity):
        self_size = self.get_area()
        other_size = other_entity.get_area()
        
        if(self_size > other_size):
            return 1
        elif(self_size < other_size):
            return -1
        else:
            return 0
        
    def get_area(self) :
        return self.rect.width * self.rect.height 

    # gets the rotation of a given point
    def rotate_point(self, point):
        rotation_radians = math.radians(self.rotation)
        x_pos = self.rect.centerx
        y_pos = self.rect.centery
        x0 = point[self.COORDINATE_X] - x_pos
        y0 = point[self.COORDINATE_Y] - y_pos
        x1 = math.cos(rotation_radians) * x0 + x_pos
        y1 = math.sin(rotation_radians) * y0 + y_pos
        return (x1, y1)

    def rotate_rect_points(self):
        rect = self.rect

        rect.topleft = self.rotate_point(rect.topleft)
        rect.topright = self.rotate_point(rect.topright)
        rect.bottomleft = self.rotate_point(rect.bottomleft)
        rect.bottomright = self.rotate_point(rect.bottomright)



class Bullet(Entity):
    def __init__(self, x, y, dir):
        Entity.__init__(self, "bullet", x, y, BULLET_WIDTH, BULLET_HEIGHT, dir)

    def move(self):
        rotation_radians = math.radians(self.rotation)
        self.rect.centerx -= BULLET_MOVEMENT*math.sin(rotation_radians)
        self.rect.centery -= BULLET_MOVEMENT*math.cos(rotation_radians)

class Gun(Entity):
    def __init__(self, ship):
        Entity.__init__(self, "gun", ship.rect.centerx, ship.rect.centery, GUN_WIDTH, GUN_HEIGHT, 0)
        print("Gun built")

class Ship(Entity):
    def __init__(self, x, y, log=False):
        Entity.__init__(self, "ship", x, y, SHIP_WIDTH, SHIP_HEIGHT, 0, log)
        self.gun = Gun(self)

    def move(self, x_delta, y_delta):
        Entity.move(self, x_delta, y_delta)
        self.gun.move(x_delta, y_delta)

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

def main():
    logging.basicConfig()
    world = World(log=True)
    world.register(Ship(100, 100, log=True))

if __name__ == "__main__":
    main()
