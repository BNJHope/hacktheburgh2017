#!/usr/bin/python

SHIP_WIDTH = 10
SHIP_HEIGHT = 10

class Entity():
    def __init__(self, identifier,  x, y, w, h, rot):
        self.identifier = identifier
        self.x_pos = x
        self.y_pos = y
        self.width = w
        self.height = h
        self.rotation = rot

    def move(self, x_delta, y_delta):
        self.x_pos = self.x_pos + x_delta
        self.y_pos = self.y_pos + y_delta

    def rotate(self, degrees):
        self.rotation += degrees


class Ship(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, "ship", x, y, SHIP_WIDTH, SHIP_HEIGHT,  0)
        print("ship built")

class World():
    def __init__(self):
        print("Created world")
        self.entities = []

    def register(self, entity):
        self.entities.append(entity)

def main():
    # logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)
    world = World()
    world.register(Ship(100, 100))
    for e in world.entities:
        print(vars(e))
        e.rotate(90)
        print(vars(e))

if __name__ == "__main__":
    main()
