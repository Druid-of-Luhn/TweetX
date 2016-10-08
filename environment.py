#!/usr/bin/env python3
import asyncio, entity, io, json, random, threading, time, websockets, whale
from random import randrange

class Environment:

    def __init__(self):
        self.spaceship = entity.Spaceship(0, 0)
        self.entities = [self.spaceship]
        # function for generating entities

    def space_contains(self, x, y):
        for entity in self.entities:
            if (entity.x-(entity.width/2) <= x <= entity.x+(entity.width/2)) and (entity.y-(entity.height/2) <= y <= entity.y+(entity.height/2)):
                return entity 
        return None
        
    def update_positions(self):
        moved_entities = []
        removed_entities = []

        for ent in self.entities:
            if ent != self.spaceship:
                ent.x -= self.spaceship.velocity_x - ent.velocity_x
                ent.y -= self.spaceship.velocity_y - ent.velocity_y

                if ent.velocity_x != 0 or ent.velocity_y != 0:
                    moved_entities.append(ent)

                entity = self.space_contains(ent.x, ent.y)
                if entity != None:
                    ent.velocity_x = -1*ent.velocity_x
                    ent.velocity_y = -1*ent.velocity_y
                    entity.velocity_x = -1*entity.velocity_x
                    entity.velocity_y = -1*entity.velocity_y

                if ent.x < 0 or ent.x > 10 or ent.y < 0 or ent.y > 10:
                    self.entities.remove(ent)
                    removed_entities.append(ent)

        # function for randomly generating new entities entering field
        return (moved_entities, removed_entities)


class Simulator:
    TICK_LENGTH = 1
    
    def __init__(self, target_address):
        self.active = False
        self.environment = Environment()
        self.target_address = target_address

    @asyncio.coroutine
    def loop(self):
        self.websocket = yield from websockets.connect(self.target_address)

        yield from self.websocket.send(json.dumps([
            {
                'entity': e.id,
                'type': type(e).__name__,
                'pos': (e.x, e.y),
                'velocity': (e.velocity_x, e.velocity_y),
                'added': True
            } for e in self.environment.entities
        ]))

        while self.active:
            moved, removed = self.environment.update_positions()
            changes = json.dumps([
                {
                    'entity': e.id,
                    'pos': (e.x, e.y),
                    'velocity': (e.velocity_x, e.velocity_y),
                } for e in moved
            ] + [
                {
                    'entity': e.id,
                    'removed': True
                } for e in removed
            ])
            
            yield from self.websocket.send(changes)
            print(changes)
            time.sleep(self.TICK_LENGTH)

    def run(self):
        self.active = True
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(self.loop())
    
    def stop(self):
        self.active = False


if __name__ == "__main__":
    sim = Simulator('ws://localhost:9000')
    sim.environment.entities += [whale.Dolphin('dolphin%d' % i, randrange(1, 10), randrange(1, 10)) for i in range(3)]
    sim.run()
