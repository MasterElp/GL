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

class Wood:
    def __init__(self):
        pass

class Mind:
    def __init__(self):
        self.action = "none"

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


class ActionSelectP(esper.Processor):
    #actions = ["say", "move", "eat", "fart", "shark_place"]
    def __init__(self):
        super().__init__()
        self.actions = [self.say, self.move, self.eat, self.fart, self.shark_place]
        self.actions_weights = [50, 100, 10, 1, 1]
        self.say_distance = 20
        self.shark_template = [ [1, 1, 1, 1, 1],
                            [1, 0, 0, 0, 1],
                            [1, 0, 0, 0, 1],
                            [1, 0, 0, 0, 1],
                            [1, 1, 2, 1, 1]]

    def process(self):
        for some, (some_mind) in self.world.get_component(Mind):
            if (some_mind.action == "none"):
                some_mind.action = random.choices(self.actions, self.actions_weights)[0]
            else:
                where = self.world.component_for_entity(some, Position)
                some_mind.action(some, where)


    def say(self, some, where):      
        for other, (other_position, other_relations) in self.world.get_components(Position, Relations):
            some_name = self.world.component_for_entity(some, Goblin).name
            other_name = self.world.component_for_entity(other, Goblin).name
            #print (other_name)
            distance = math.sqrt((where.x - other_position.x)**2 + (where.y - other_position.y)**2)

            if (distance <= self.say_distance):
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
        places = self.world.get_component(Place)
        if (len(places) <= 0):
            for y in range (len(self.shark_template)): 
                for x in range (len(self.shark_template[y])):
                    if (self.shark_template[y][x] == 1):
                        self.world.create_entity(Place("wall"), Position(where.x + x, where.y + y), Paint(200, 150, 150, 50))
                    elif (self.shark_template[y][x] == 2):
                        self.world.create_entity(Place("door"), Position(where.x + x, where.y + y), Paint(200, 200, 150, 50))




'''
class Search_aim(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        #print("Search_aim")
        for user_entity, (user, position, aim) in self.world.get_components(User, Position, Aim):
            if(not aim.has_aim):
                min_distance = 1000
                found = False
                #print("user_entity")
                #print(user_entity)
                for block_entity, (block, block_position, stocked, busy) in self.world.get_components(Block, Position, Stocked, Busy):
                    if ((not stocked.is_true) and (not busy.is_true)):
                        found = True
                        #distance = math.sqrt((block_position.x - position.x)**2 + (block_position.y - position.y)**2)
                        distance = 0
                        if (distance < min_distance):
                            min_distance = distance
                            near_x = block_position.x
                            near_y = block_position.y
                            near_entity = block_entity

                if (found):
                    #print("near_entity")
                    #print(near_entity)
                    aim.has_aim = True
                    aim.x = near_x
                    aim.y = near_y
                    aim.entity = near_entity
                    near_busy = self.world.component_for_entity(near_entity, Busy)
                    near_busy.is_true = True


class Move(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        #print("move")
        for user_entity, (user, position, aim) in self.world.get_components(User, Position, Aim):
            if (aim.has_aim):
                if (position.x == aim.x and position.y == aim.y):
                    aim.has_aim = False
                    busy = self.world.component_for_entity(aim.entity, Busy)
                    busy.is_true = False
                    pass
                else:
                    if (position.x > aim.x):
                        position.x-=1
                    elif (position.x < aim.x):
                        position.x+=1
                    if (position.y > aim.y):
                        position.y-=1
                    elif (position.y < aim.y):
                        position.y+=1

class Haul(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        #print("haul")
        for user_entity, (user, position, aim) in self.world.get_components(User, Position, Aim):
            for block_entity, (block, block_position, stocked, busy) in self.world.get_components(Block, Position, Stocked, Busy):
                if (position.x == block_position.x and position.y == block_position.y and not stocked.is_true):
                    min_distance = 1000
                    found = False
                    for stock_entity, (stock, stock_position, full) in self.world.get_components(Stock, Position, Full):
                        if (not full.is_true):
                            found = True
                            #distance = math.sqrt((block_position.x - position.x)**2 + (block_position.y - position.y)**2)
                            distance = 0
                            if (distance < min_distance):
                                min_distance = distance
                                near_x = stock_position.x
                                near_y = stock_position.y

                    if (found):
                        if (block_position.x > near_x):
                            block_position.x-=1
                        elif (block_position.x < near_x):
                            block_position.x+=1
                        if (block_position.y > near_y):
                            block_position.y-=1
                        elif (block_position.y < near_y):
                            block_position.y+=1
                        


class Stock_check(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for block_entity, (block, block_position, stocked) in self.world.get_components(Block, Position, Stocked):
            for stock_entity, (stock, stock_position, full) in self.world.get_components(Stock, Position, Full):
                if (not full.is_true and not stocked.is_true):
                    if (block_position.x == stock_position.x and block_position.y == stock_position.y):
                        full.is_true = True
                        stocked.is_true = True
                        #print("!!!++++++!!!")
'''

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
        wood = world.create_entity(Wood(), Owner(goblin), Position(random.randint(40, 80), random.randint(10, 50)), Paint(250, 150, 150, 100))
        #huts.append(hut)

    # Instantiate a Processor (or more), and add them to the world:
    #world.add_processor(UserInterfaceP(user))
    world.add_processor(ActionSelectP())
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
            world.get_processor(ShowP).process()



if __name__ == "__main__":
    main()