#!/usr/bin/python

class Entity():
    def __init__(self, identifier,  x, y):
        self.identifier = identifier
        self.x_pos = x
        self.y_pos = y
        print("entity built")

    def identify(self):
        print("I am an entity")

class Ship(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, "ship", x, y)
        print("ship built")

    def identify(self):
        print("I am an ship")

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

if __name__ == "__main__":
    main()
