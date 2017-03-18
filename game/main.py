#!/usr/bin/python

import logging

SHIP_WIDTH = 50
SHIP_HEIGHT = 50

GUN_WIDTH = 5
GUN_HEIGHT = 75

class Entity():
    def __init__(self, identifier,  x, y, w, h, rot, log=False):
        self.identifier = identifier
        self.x_pos = x
        self.y_pos = y
        self.width = w
        self.height = h
        self.rotation = rot
        if log:
            self.logger = logging.getLogger("world.{}".format(self.identifier))
            self.logger.setLevel(logging.INFO)
            self.logger.info("created entity")



    def move(self, x_delta, y_delta):
        self.x_pos = self.x_pos + x_delta
        self.y_pos = self.y_pos + y_delta

    def rotate(self, degrees):
        self.rotation += degrees

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
        return self.width * self.height
        

class Gun(Entity):
    def __init__(self, ship):
        Entity.__init__(self, "gun", ship.x_pos, ship.y_pos, GUN_WIDTH, GUN_HEIGHT, 0)
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
