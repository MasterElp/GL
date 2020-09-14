import esper
import time
import random

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


class PositionProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        self.show_all_locations()
        pass

    def location_contain(self, location):
        objects_contain = []
        for inside_object, position in self.world.get_component(Position):
            if (position.location == location):
                objects_contain.append(inside_object)

        return objects_contain

    def show_all_locations(self):
        for entity, location in self.world.get_components(Location):
            print("location: ", entity)
            print(self.location_contain(entity))

"""class Vision:
    def __init__(self):
        self.objects_count = 0

class MovementProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (vel, pos) in self.world.get_components(Velocity, Position):
            #pos.x += vel.x
            #pos.y += vel.y
            #print("Current Position: {}".format((int(pos.x), int(pos.y))))
            pass

class VisionProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        print("X")
        for ent, (vision, my_pos) in self.world.get_components(Vision, Position):
            vision.objects_count = 0
            print("My position: {}".format((int(my_pos.x), int(my_pos.y))))
            for other, pos in self.world.get_component(Position):
                #print("other: {}".format((int(pos.x), int(pos.y))))
                if ((my_pos.x != pos.x) and (my_pos.y != pos.y)):
                    vision.objects_count += 1
                    print("Other object: {}".format((other, int(pos.x), int(pos.y))))"""



def main():
    # Create a World instance to hold everything:
    world = esper.World()

    # Instantiate a Processor (or more), and add them to the world:
    movement_processor = PositionProcessor()
    world.add_processor(movement_processor)

    area = world.create_entity(Location())
    glade = world.create_entity(Location(), Position(area))
    home = world.create_entity(Location(), Position(area))


    goblin = []
    # Create entities, and assign Component instances to them:
    for i in range(10):
        goblin.append(world.create_entity(Relations(), Position(glade)))
        #world.add_component(player[i], Velocity(x=0.9, y=1.2))
        #world.add_component(player[i], Position(x=5, y=5))
        #world.add_component(player[i], Vision())



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