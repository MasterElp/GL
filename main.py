# Install: python 3.8.5, pip install pygame(2.0.1), pip install keyboard, load esper version = '1.3'
import graph
import esper
import time
import random
import keyboard


class Interface:
    step_number = 0
    pause = False

    def __init__(self):
        graph.SCALE = 10
        self.map_x = Map.AREA_X * graph.SCALE
        self.map_y = Map.AREA_Y * graph.SCALE
        graph.init_window((self.map_x + 400), (self.map_y + 200), "My own little world")

    def step(self):
        graph.blit()
        graph.screen_text('step: ' + str(self.step_number), 20, (self.map_y + 60))

    def pause_pressed(self, e):
        if (self.pause):        
            self.pause = False
            print ("start")
        else:
            self.pause = True
            print ("pause")

class Roll:
    @staticmethod
    def dice_1000(c_probability):
        dice = random.randint(0, 1000)
        if dice <= c_probability:
            return True
        else:
            return False

class Map:
    AREA_X = 80
    AREA_Y = 60

    @staticmethod
    def tor(c_x, c_y):
        if c_x >= Map.AREA_X:
            c_x -= Map.AREA_X
        elif c_x < 0:
            c_x -= Map.AREA_X
        if c_y >= Map.AREA_Y:
            c_y -= Map.AREA_Y
        elif c_y < 0:
            c_y -= Map.AREA_Y
        return c_x, c_y

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

class Mind:
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
        for entity, (position, paint) in self.world.get_components(Position, Paint):
            graph.draw_rect(position.x, position.y, paint.color, paint.alfa)


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
        #where = self.world.try_component(some, Position).location

        word = self.world.create_entity(Timer(5), Owner(some))
        some_name = self.world.component_for_entity(some, Goblin).name
        print(f"{some_name} сказал слово: {word}")
        
    def move(self, some):
        for entity, (position, mind) in self.world.get_components(Position, Mind):
            position.x += random.randint(-1, 1)
            position.y += random.randint(-1, 1)

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
        for some, (some_relations) in self.world.get_component(Relations):
            #print("some: ", some)
            for other, (other_relations) in self.world.get_component(Relations):
                #print("other: ", other)              
                #print("some_position: ", some_position.location)
                #print(some_relations.relations2others)
                if (other in some_relations.relations2others):
                    some_relations.relations2others[other] += random.randint(-1, 1)
                else:
                    some_relations.relations2others[other] = 0


class UserInterfaceP(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        pass




def main():
    global pause
    pause = False
    # Create a World instance to hold everything:
    world = esper.World()
    inter = Interface()
    random.seed()

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
    keyboard.on_release_key('enter', inter.pause_pressed)

    # A dummy main loop:
    try:
        while True:
            inter.step_number += 1
            inter.step()

            # Call world.process() to run all Processors.
            world.process()
            graph.flip()
            time.sleep(0.5)
            
            while (pause):
                pass

    except KeyboardInterrupt:
        return



if __name__ == "__main__":
    main()