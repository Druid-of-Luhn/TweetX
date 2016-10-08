#!/usr/bin/env python3
import asyncio, entity, io, json, queue, random, threading, time, websockets, whale
from bot import bot
from random import randrange

class Event:
    def __init__(self):
        self.callbacks = []

    def __call__(self, *a, **kw):
        for callback in self.callbacks:
            callback(*a, **kw)

    def __iadd__(self, callback):
        self.callbacks.append(callback)
        return self


class Environment:
    def __init__(self):
        self.spaceship = entity.Spaceship(0, 0)
        self.entities = [self.spaceship]

        self.entity_added = Event()
        self.entity_removed = Event()
        self.entity_moved = Event()


    def add_entity(self, entity):
        self.entities.append(entity)
        self.entity_added(entity)

    def remove_entity(self, entity):
        self.entities.remove(entity)
        self.entity_removed(entity)
        

    def space_contains(self, x, y):
        for entity in self.entities:
            if (entity.x-(entity.width/2) <= x <= entity.x+(entity.width/2)) and (entity.y-(entity.height/2) <= y <= entity.y+(entity.height/2)):
                return entity 
        return None
        
    def update_positions(self):
        for ent in self.entities:
            if ent != self.spaceship:
                ent.x -= self.spaceship.velocity_x - ent.velocity_x
                ent.y -= self.spaceship.velocity_y - ent.velocity_y

                if ent.velocity_x != 0 or ent.velocity_y != 0:
                    self.entity_moved(ent)

                entity = self.space_contains(ent.x, ent.y)
                if entity != None:
                    ent.velocity_x = -1*ent.velocity_x
                    ent.velocity_y = -1*ent.velocity_y
                    entity.velocity_x = -1*entity.velocity_x
                    entity.velocity_y = -1*entity.velocity_y

                #if ent.x < 0 or ent.x > 10 or ent.y < 0 or ent.y > 10:
                    #self.remove_entity(ent)


class Game:
    # The internal tick length, in seconds
    TICK_LENGTH = 1
    # The number of internal ticks to a command tick
    TICKS_PER_COMMAND_TICK = 5
    
    def __init__(self, host = 'localhost', port = 17922):
        self.active = False
        self.environment = Environment()
        self.host = host
        self.port = port
        self.clients = []
        self.changes = queue.Queue()
        self.ticks_since_last_command = 0
        self.bot = bot.TwitterBot(self)
        self.exit_event = threading.Event()

        self.environment.entity_added += self.handle_entity_added
        self.environment.entity_removed += self.handle_entity_removed
        self.environment.entity_moved += self.handle_entity_moved


    def handle_entity_added(self, e):
        self.changes.put({
            'entity': e.id,
            'type': type(e).__name__,
            'pos': (e.x, e.y),
            'velocity': (e.velocity_x, e.velocity_y),
            'added': True
        })

    def handle_entity_removed(self, e):
        self.changes.put({
            'entity': e.id,
            'removed': True
        })

    def handle_entity_moved(self, e):
        self.changes.put({
            'entity': e.id,
            'pos': (e.x, e.y),
            'velocity': (e.velocity_x, e.velocity_y),
        })


    @asyncio.coroutine
    def new_client(self, client):
        self.clients.append(client)
        self.exit_event.wait()
        self.clients.remove(client)

    @asyncio.coroutine
    def loop(self):
        self.websocket = yield from websockets.serve(self.new_client, self.host, self.port)

        while self.active:
            if self.ticks_since_last_command == 0:
                self.bot.tick()
                self.ticks_since_last_command = self.TICKS_PER_COMMAND_TICK
            else:
                self.ticks_since_last_command -= 1
            self.environment.update_positions()

            while True:
                try:
                    change = self.changes.get_nowait()
                except queue.Empty:
                    break
                
                for client in self.clients:
                    yield from client.send(json.dumps(change))

                print(change)

            time.sleep(self.TICK_LENGTH)

    def run(self):
        self.active = True
        self.bot.start()
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(self.loop())
    
    def stop(self):
        self.active = False
        self.exit_event.set()


if __name__ == "__main__":
    sim = Game()
    [sim.environment.add_entity(whale.Dolphin('dolphin%d' % i, randrange(1, 10), randrange(1, 10))) for i in range(3)]
    sim.run()
