#!/usr/bin/python

class Entity():
    def __init__(self):
       print("entity built")

    def identify(self):
        print("I am an entity")

class Ship(Entity):
    def __init__(self):
        Entity.__init__(self)
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
    world = World()
    world.register(Ship())
    print(world.entities)

if __name__ == "__main__":
    main()
