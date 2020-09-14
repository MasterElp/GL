#pip install keyboard
import esper
import time
import random
import keyboard

names = ["asd", "sasd", "sasder", "qwe", "sdsac"]

class Name:
    def __init__(self, name=None):
        if (name == None):
            self.name = random.choice(names)
        else:
            self.name = name

class User:
    def __init__(self):
        pass

class Relations:
    def __init__(self):
        pass

# Location can content units fnd other locations
class Location:
    def __init__(self):
        pass

class Position:
    def __init__(self, location):
        self.location = location

class UserInterfaceProcessor(esper.Processor):
    def __init__(self, user):
        super().__init__()
        self.user = user

    def process(self):
        #for user, user_component in self.world.get_component(User):
        
        if keyboard.is_pressed("p"):
            print("You pressed p")
        if keyboard.is_pressed("s"): #show
            location = self.world.component_for_entity(self.user, Position).location
            print("location: ", location)
            print(location_contain(self.world, location))


class PositionProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        #self.show_all_locations()
        pass

    def show_all_locations(self):
        for entity, location in self.world.get_components(Location):
            print("location: ", entity)
            print(location_contain(self.world, entity))


def location_contain(world, location):
    objects_contain = []
    for inside_object, position in world.get_component(Position):
        if (position.location == location):
            if (world.has_component(inside_object, Name)):
                objects_contain.append(world.component_for_entity(inside_object, Name).name)
            else:
                objects_contain.append(inside_object)

    return objects_contain

def main():
    # Create a World instance to hold everything:
    world = esper.World()

    area = world.create_entity(Location())
    glade = world.create_entity(Location(), Position(area))
    home = world.create_entity(Location(), Position(area))

    user = world.create_entity(User(), Relations(), Position(area), Name("user"))

    goblin = []
    # Create entities, and assign Component instances to them:
    for i in range(10):
        goblin.append(world.create_entity(Relations(), Position(glade), Relations(), Name()))
        #world.add_component(player[i], Velocity(x=0.9, y=1.2))
        #world.add_component(player[i], Position(x=5, y=5))
        #world.add_component(player[i], Vision())

    # Instantiate a Processor (or more), and add them to the world:
    world.add_processor(PositionProcessor())
    world.add_processor(UserInterfaceProcessor(user))


    # A dummy main loop:
    try:
        while True:
            # Call world.process() to run all Processors.
            world.process()
            time.sleep(1)

    except KeyboardInterrupt:
        return



if __name__ == "__main__":
    main()