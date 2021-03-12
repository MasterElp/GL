# Install: python 3.8.5, pip install pygame(2.0.1), pip install keyboard, load esper version = '1.3'
import keyboard

import graph
import esper

import time
import random
import math

class Roll:
    @staticmethod
    def dice_1000(c_probability):
        dice = random.randint(0, 1000)
        if dice <= c_probability:
            return True
        else:
            return False

class Interface:
    step_number = 0
    map_x = 800
    map_y = 600
    pause_game = False
    exit_game = False

    def __init__(self):
        graph.Map.scale = 10
        graph.Map.area_x = 80
        graph.Map.area_y = 60
        self.map_x = graph.Map.area_x * graph.Map.scale
        self.map_y = graph.Map.area_y * graph.Map.scale
        graph.init_window(self.map_x + 400, self.map_y + 200, "My own little world")


class Position:
    def __init__(self, x_, y_):
        self.x = x_
        self.y = y_

class Paint:
    """Init entity color (r, g, b, alfa)"""
    def __init__(self, r_=50, g_=50, b_=50, alfa_=50):  
        self.color = (r_, g_, b_)
        self. alfa = alfa_

class Owner:
     def __init__(self, entity):
        self.entity = entity

class Goblin:
    def __init__(self, name=None):
        male_names = ["Сап", "Нуур", "Зид", "Бердж", "Домл", "Гог", "Мог", "Бууб", "Дир", "Мак"]
        female_names = ["Бер", "Нуур", "Оёни", "Ига", "Домл", "Зиз", "Оёри", "Сав", "Дир", "Мал"]
        male_names_weights = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        female_names_weights = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

        if (name == None):
            self.name = random.choices(male_names + female_names, male_names_weights + female_names_weights)[0]
        else:
            self.name = name

class Room:
    def __init__(self):
        pass

class Mind:
    def __init__(self):
        pass

class User:
    def __init__(self):
        pass

class Relations:
    def __init__(self):
        self.relations2others = {}
        pass

class Communication:
    def __init__(self):
        pass

class Timer:
    def __init__(self, kill_time):
        self.kill_time = kill_time
        self.timer = 0

class Place:
    def __init__(self, object_type):
        self.object_type = type


class ShowP(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        graph.clear_screen()
        (inter_entity, inter) = self.world.get_component(Interface)[0]
        inter.step_number += 1
        graph.screen_text('step: ' + str(inter.step_number), 20, (inter.map_y + 60))
        for entity, (position, paint) in self.world.get_components(Position, Paint):
            graph.draw_rect(position.x, position.y, paint.color, paint.alfa)
        graph.update()

class TimeP(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for some, (some_timer) in self.world.get_components(Timer):
            some_timer = self.world.component_for_entity(some, Timer)

            some_timer.timer += 1
            if (some_timer.timer >= some_timer.kill_time):
                #print(f"{some} deleted")
                self.world.delete_entity(some)


class ThinkP(esper.Processor):
    def __init__(self):
        super().__init__()
        self.actions = [self.say, self.move, self.eat, self.fart, self.shark_place]
        self.actions_weights = [50, 100, 10, 1, 1]
        self.say_distance = 10

    def say(self, some, where):      
        for other, (other_position, other_relations) in self.world.get_components(Position, Relations):
            distance = math.sqrt((where.x - other_position.x)**2 + (where.y - other_position.y)**2)
            if (distance > self.say_distance):
                some_name = self.world.component_for_entity(some, Goblin).name
                other_name = self.world.component_for_entity(other, Goblin).name
                #print(f"{some_name} сказал слово {other_name}.")

                if (some in other_relations.relations2others):
                    other_relations.relations2others[some] += random.randint(-1, 1)
                else:
                    other_relations.relations2others[some] = 0
        
    def move(self, some, where):
        x, y = graph.tor(where.x + random.randint(-1, 1), where.y + random.randint(-1, 1))
        where.x = x
        where.y = y

    def fart(self, some, where):
        stench = self.world.create_entity(Timer(10), Position(where.x, where.y), Paint(200, 200))
        some_name = self.world.component_for_entity(some, Goblin).name
        #print(f"{some_name} сказал слово: {stench}")

    def eat(self, some, where):
        #print("Съел")
        pass

    def shark_place(self, some, where):
        template = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
        ]

        for y in range (len(template)): 
            for x in range (len(template[y])):
                if (template[y][x] == 1):
                    self.world.create_entity(Place("wall"), Position(where.x + x, where.y + y), Paint(200, 150, 150, 100))



    def process(self):
        for some, (some_mind) in self.world.get_components(Mind):
            where = self.world.component_for_entity(some, Position)

            action = random.choices(self.actions, self.actions_weights)
            action[0](some, where)



def exit_pressed(world, interface):
    world.component_for_entity(interface, Interface).exit_game = True

def pause_pressed(world, interface):
    if (world.component_for_entity(interface, Interface).pause_game):        
        world.component_for_entity(interface, Interface).pause_game = False
    else:
        world.component_for_entity(interface, Interface).pause_game = True
        print ("pause_game")

def main():
    # Create a World instance to hold everything:
    world = esper.World()
    
    random.seed()

    interface = world.create_entity(Interface())
    user = world.create_entity(User(), Goblin("Игрок"), Relations(), Position(10, 10), Paint(250, 250, 250))

    goblins = []
    huts = []
    # Create entities, and assign Component instances to them:
    for i in range(10):
        goblin = world.create_entity(Goblin(), Mind(), Relations(), Position(random.randint(40, 80), random.randint(10, 50)), Paint(150, 150, 150, 100))
        #goblins.append(goblin)
        hut = world.create_entity(Room(), Owner(goblin), Position(random.randint(40, 80), random.randint(10, 50)), Paint(250, 150, 150, 100))
        #huts.append(hut)

    # Instantiate a Processor (or more), and add them to the world:
    #world.add_processor(UserInterfaceP(user))
    world.add_processor(ThinkP())
    world.add_processor(TimeP())
    world.add_processor(ShowP())

    #keyboard.add_hotkey('space', print, args=['space was pressed'])
    #keyboard.add_hotkey('ctrl+alt+enter, space', some_callback)
    keyboard.add_hotkey('r', print, args=[world.component_for_entity(user, Relations).relations2others])
    keyboard.add_hotkey('enter', pause_pressed, args=[world, interface])
    keyboard.add_hotkey('esc', exit_pressed, args=[world, interface])


    while (world.component_for_entity(interface, Interface).exit_game == False):
        world.process()
        
        #time.sleep(0.5)
        while (world.component_for_entity(interface, Interface).pause_game):
            pass



if __name__ == "__main__":
    main()