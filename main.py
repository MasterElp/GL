#pip install keyboard
import esper
import time
import random
import keyboard

names = ["asd", "sasd", "sasder", "qwe", "sdsac"]
actions = ["said", "move", "nothing", "eat"]

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
        self.relations2others = {}
        pass

# Location can content units and other locations
class Location:
    def __init__(self):
        pass

class Position:
    def __init__(self, location):
        self.location = location

class Communication:
    def __init__(self):
        pass

class Mind:
    def __init__(self):
        pass

class ThinkP(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for some, (some_mind) in self.world.get_components(Mind):
            action = random.choice(actions)
            if (action == "said"):
                pass

            
                    


class RelationsP(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for some, (some_relations, some_position) in self.world.get_components(Relations, Position):
            #print("some: ", some)
            for other, (other_relations, other_position) in self.world.get_components(Relations, Position):
                if (some_position.location == other_position.location):
                    #print("other: ", other)              
                    #print("some_position: ", some_position.location)
                    #print(some_relations.relations2others)
                    if (other in some_relations.relations2others):
                        some_relations.relations2others[other] += random.randint(-1, 1)
                    else:
                        some_relations.relations2others[other] = 0


class UserInterfaceP(esper.Processor):
    def __init__(self, user):
        super().__init__()
        self.user = user

    def process(self):
        #for user, user_component in self.world.get_component(User):
        if keyboard.is_pressed("p"):
            print("You pressed p")
        if keyboard.is_pressed("s"): #show location
            user_position = self.world.component_for_entity(self.user, Position).location
            print("user_position: ", user_position)
            print(location_contain(self.world, user_position))
        if keyboard.is_pressed("r"): #show relations
            print(self.world.component_for_entity(self.user, Relations).relations2others)


def show_all_locations(world):
    for entity, location in world.get_component(Location):
        print("location: ", entity)
        print(location_contain(world, entity))

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
    random.seed() 

    area = world.create_entity(Location())
    glade = world.create_entity(Location(), Position(area))
    home = world.create_entity(Location(), Position(area))

    user = world.create_entity(User(), Relations(), Position(home), Name("user"))

    goblins = []
    # Create entities, and assign Component instances to them:
    for i in range(6):
        goblins.append(world.create_entity(Relations(), Relations(), Name(), Mind()))
    for i in range(4):
        goblins.append(world.create_entity(Relations(), Relations(), Name(), Mind()))

    for goblin in goblins:
        if (random.choice([True, False])):
            world.add_component(goblin, Position(glade))
        else:
            world.add_component(goblin, Position(home))


    # Instantiate a Processor (or more), and add them to the world:
    #world.add_processor(PositionProcessor())
    world.add_processor(UserInterfaceP(user))
    world.add_processor(RelationsP())


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