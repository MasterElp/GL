#pip install keyboard
import esper
import time
import random
import keyboard

names = ["Sap", "Noor", "Zid", "Berj", "Doml", "Gog", "Mog", "Boob", "Dir", "Mak"]
names_weights = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

class Name:
    def __init__(self, name=None):
        if (name == None):
            self.name = random.choices(names, names_weights)
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

class Timer:
    def __init__(self, kill_time):
        self.kill_time = kill_time
        self.timer = 0


class TimeP(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for some, (some_timer) in self.world.get_components(Timer):
            some_timer = self.world.component_for_entity(some, Timer)

            some_timer.timer += 1
            if (some_timer.timer >= some_timer.kill_time):
                print(f"{some} deleted")
                self.world.delete_entity(some)



class ThinkP(esper.Processor):
    def __init__(self):
        super().__init__()
        self.actions = [self.say, self.move, self.eat]
        self.actions_weights = [0, 100, 10]

    def say(self, some):
        #where = self.world.try_component(some, Position).location
        location_of_some = self.world.component_for_entity(some, Position).location
        word = self.world.create_entity(Position(location_of_some), Timer(5))
        print(f"{some} say in {location_of_some} word {word}")
        
    def move(self, some):
        can_move_locations = []
        position_of_some = self.world.component_for_entity(some, Position)
        location_of_some = position_of_some.location

        for parent_position in self.world.try_component(location_of_some, Position):
            can_move_locations.append(parent_position.location)
        for child_location, (position, is_location) in self.world.get_components(Position, Location):
            if (position.location == location_of_some):
                can_move_locations.append(child_location)
        #print(f"{some} from {location_of_some} can move {can_move_locations}")

        move_to = random.choice(can_move_locations)
        position_of_some.location = move_to
        print(f"{some} from {location_of_some} move to {move_to}")

    def eat(self, some):
        print("eat")

    def process(self):
        for some, (some_mind) in self.world.get_components(Mind):
            action = random.choices(self.actions, self.actions_weights)
            action[0](some)


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
        user_position = self.world.component_for_entity(self.user, Position).location
        print("user_position: ", user_position)
        print(location_contain(self.world, user_position))

        #if keyboard.is_pressed("r"): #show relations
        #    print(self.world.component_for_entity(self.user, Relations).relations2others)


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

def pause_pressed(e):
    global pause
    if (pause):        
        pause = False
        print ("start")
    else:
        pause = True
        print ("pause")


def main():
    global pause
    pause = False
    # Create a World instance to hold everything:
    world = esper.World()
    random.seed()

    area = world.create_entity(Location())
    glade = world.create_entity(Location(), Position(area))
    home = world.create_entity(Location(), Position(area))

    user = world.create_entity(User(), Relations(), Position(home), Name("user"))

    goblins = []
    # Create entities, and assign Component instances to them:
    for i in range(10):
        goblins.append(world.create_entity(Relations(), Position(random.choice([glade, home, area])), Relations(), Name(), Mind()))

    # Instantiate a Processor (or more), and add them to the world:
    #world.add_processor(PositionProcessor())
    world.add_processor(UserInterfaceP(user))
    world.add_processor(RelationsP())
    world.add_processor(ThinkP())
    world.add_processor(TimeP())

    #keyboard.add_hotkey('space', print, args=['space was pressed'])
    #keyboard.add_hotkey('ctrl+alt+enter, space', some_callback)
    keyboard.add_hotkey('r', print, args=[world.component_for_entity(user, Relations).relations2others])
    keyboard.on_release_key('enter', pause_pressed)

    # A dummy main loop:
    try:
        while True:
            # Call world.process() to run all Processors.
            world.process()
            time.sleep(1)
            
            while (pause):
                pass

    except KeyboardInterrupt:
        return



if __name__ == "__main__":
    main()