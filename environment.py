#!/usr/bin/env python3
import asyncio, entity, io, json, queue, random, threading, time, websockets, whale
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
    
    def __init__(self, target_address):
        self.active = False
        self.environment = Environment()
        self.target_address = target_address
        self.changes = queue.Queue()

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
    def loop(self):
        self.websocket = yield from websockets.connect(self.target_address)

        while self.active:
            self.environment.update_positions()

            while True:
                try:
                    change = self.changes.get_nowait()
                    if change is None:
                        break
                except queue.Empty:
                    break
                
                yield from self.websocket.send(json.dumps(change))
                print(change)

            time.sleep(self.TICK_LENGTH)

    def run(self):
        self.active = True
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(self.loop())
    
    def stop(self):
        self.active = False


if __name__ == "__main__":
    sim = Game('ws://localhost:9000')
    [sim.environment.add_entity(whale.Dolphin('dolphin%d' % i, randrange(1, 10), randrange(1, 10))) for i in range(3)]
    sim.run()
