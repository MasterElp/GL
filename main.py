# Install: python 3.8.5, pip install pygame(2.0.1), pip install keyboard, load esper version = '1.3'
import graph
import esper
import time
import random
import keyboard

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
    pause = False

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
                print(f"{some} deleted")
                self.world.delete_entity(some)


class ThinkP(esper.Processor):
    def __init__(self):
        super().__init__()
        self.actions = [self.say, self.move, self.eat]
        self.actions_weights = [50, 100, 10]

    def say(self, some):
        where_x = self.world.component_for_entity(some, Position).x
        where_y = self.world.component_for_entity(some, Position).y
        

        word = self.world.create_entity(Timer(5), Owner(some), Position(where_x, where_y), Paint(250))
        some_name = self.world.component_for_entity(some, Goblin).name
        print(f"{some_name} сказал слово: {word}")
        
    def move(self, some):
        for entity, (position, mind) in self.world.get_components(Position, Mind):
            x, y = graph.tor(position.x + random.randint(-1, 1), position.y + random.randint(-1, 1))
            position.x = x
            position.y = y

    def eat(self, some):
        print("Съел")

    def process(self):
        for some, (some_mind) in self.world.get_components(Mind):
            action = random.choices(self.actions, self.actions_weights)
            action[0](some)


class RelationsP(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for some, (some_relations) in self.world.get_component(Relations):
            #print("some: ", some)
            for other, (other_relations) in self.world.get_component(Relations):
                #print("other: ", other)              
                #print(some_relations.relations2others)
                if (other in some_relations.relations2others):
                    some_relations.relations2others[other] += random.randint(-1, 1)
                else:
                    some_relations.relations2others[other] = 0





def pause_pressed(world, interface):
    if (world.component_for_entity(interface, Interface).pause):        
        world.component_for_entity(interface, Interface).pause = False
    else:
        world.component_for_entity(interface, Interface).pause = True
        print ("pause")

def main():
    # Create a World instance to hold everything:
    world = esper.World()
    
    random.seed()

    interface = world.create_entity(Interface())
    user = world.create_entity(User(), Goblin("Игрок"), Relations(), Position(10, 10), Paint(250, 250, 250))

    goblins = []
    # Create entities, and assign Component instances to them:
    for i in range(10):
        goblins.append(world.create_entity(Goblin(), Mind(), Relations(), Position(random.randint(40, 80), random.randint(10, 50)), Paint(150, 150, 150, 100)))

    # Instantiate a Processor (or more), and add them to the world:
    #world.add_processor(UserInterfaceP(user))
    world.add_processor(RelationsP())
    world.add_processor(ThinkP())
    world.add_processor(TimeP())
    world.add_processor(ShowP())

    #keyboard.add_hotkey('space', print, args=['space was pressed'])
    #keyboard.add_hotkey('ctrl+alt+enter, space', some_callback)
    keyboard.add_hotkey('r', print, args=[world.component_for_entity(user, Relations).relations2others])
    #keyboard.on_release_key('enter', pause_pressed)
    keyboard.add_hotkey('enter', pause_pressed, args=[world, interface])


    while True:
        world.process()
        
        #time.sleep(0.5)
        while (world.component_for_entity(interface, Interface).pause):
            pass



if __name__ == "__main__":
    main()