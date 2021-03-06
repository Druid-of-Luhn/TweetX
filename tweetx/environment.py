#!/usr/bin/env python3
import asyncio, entity, io, json, logging, queue, random, threading, time, websockets, whale
from bot import bot
from random import randrange

logging.basicConfig()
log = logging.getLogger('tweetx')
log.setLevel(logging.DEBUG)


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
        self.spaceship = entity.Spaceship(self, 0, 0)
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
            ent.tick()
            ent.x += ent.velocity_x
            ent.y += ent.velocity_y

            if ent.velocity_x != 0 or ent.velocity_y != 0:
                self.entity_moved(ent)

            collide_entity = self.space_contains(ent.x, ent.y)
            if entity != None:
                ent.velocity_x = -1*ent.velocity_x
                ent.velocity_y = -1*ent.velocity_y
                collide_entity.velocity_x = -1*collide_entity.velocity_x
                collide_entity.velocity_y = -1*collide_entity.velocity_y
                if isinstance(collide_entity, entity.Spaceship):
                    collide_entity.health -= 1
                if isinstance(collide_entity, entity.Spaceship):
                    collide_entity.health -= 1

    def generate_entities(self):
        appearance_probabilities = (
            (0.15, lambda: random.choice([whale.Dolphin])),
            (0.1, lambda: entity.Meteor),
            (0.05, lambda: entity.Planet)
        )

        k = random.uniform(0, 1)
        for p, choose in appearance_probabilities:
            if p > k:
                while True:
                    dx = (1 if random.uniform(0, 1) > 0.5 else -1) * max(0, random.uniform(80, 500))
                    dy = (1 if random.uniform(0, 1) > 0.5 else -1) * max(0, random.uniform(80, 500))
                    new_entity = choose()(self.spaceship.x + dx, self.spaceship.y + dy)

                    if self.space_contains(new_entity.x, new_entity.y) is None:
                        break

                self.add_entity(new_entity)
                log.debug('Generated a %s at (%s, %s)' % (type(new_entity).__name__, new_entity.x, new_entity.y))
                break

class Game:
    class Client:
        def __init__(self, game, websocket, path):
            self.game = game
            self.websocket = websocket
            self.path = path
            self.queue = queue.Queue()

        def push(self, change):
            if self.game.active:
                log.debug('Sending to %s: %s' % (self.websocket.remote_address, change))
                self.queue.put(change)

        async def loop(self):
            while self.game.active:
                change = self.queue.get()
                await self.websocket.send(json.dumps(change))

            self.game.clients.remove(self)

        def handle_entity_added(self, e):
            self.push({
                'entity': e.id,
                'type': type(e).__name__,
                'pos': (e.x, e.y),
                'velocity': (e.velocity_x, e.velocity_y),
                'width': e.width,
                'height': e.height,
                'direction': e.direction_orientation,
                'added': True
            })

        def handle_entity_removed(self, e):
            self.push({
                'entity': e.id,
                'removed': True
            })

        def handle_entity_moved(self, e):
            self.push({
                'entity': e.id,
                'pos': (e.x, e.y),
                'width': e.width,
                'height': e.height,
                'velocity': (e.velocity_x, e.velocity_y),
                'direction': e.direction_orientation,
            })


    # The internal tick length, in seconds
    TICK_LENGTH = 0.5
    # The number of internal ticks to a command tick
    TICKS_PER_COMMAND_TICK = 10
    
    def __init__(self, host = 'localhost', port = 17922):
        self.active = False
        self.environment = Environment()
        self.host = host
        self.port = port
        self.clients = []
        self.changes = queue.Queue()
        self.ticks = 0
        self.ticks_since_last_command = 0
        self.bot = bot.TwitterBot(self)
        self.exit_event = threading.Event()


    async def start_server(self):
        async def new_client(websocket, path):
            log.info('New client! %s' % (websocket.remote_address,))

            client = self.Client(self, websocket, path)
            self.clients.append(client)
            self.environment.entity_added += client.handle_entity_added
            self.environment.entity_removed += client.handle_entity_removed
            self.environment.entity_moved += client.handle_entity_moved

            for entity in self.environment.entities:
                client.handle_entity_added(entity)

            await client.loop()

        self.websocket = await websockets.serve(new_client, self.host, self.port)
        log.info('Started listening on %s:%d' % (self.host, self.port))

    def tick(self):
        while self.active:
            self.ticks += 1
            log.debug('Tick!')

            for client in self.clients:
                client.push({
                    'power': self.environment.spaceship.reactor.power,
                    'shield': self.environment.spaceship.shield.charge,
                    'engines': self.environment.spaceship.engine_power.charge,
                    'weapon': self.environment.spaceship.weapon.charge
                })

            if self.ticks_since_last_command == 0:
                log.debug('Performing a command tick...')
                self.bot.tick()
                self.ticks_since_last_command = self.TICKS_PER_COMMAND_TICK
            else:
                self.ticks_since_last_command -= 1

            self.environment.update_positions()
            self.environment.generate_entities()
            time.sleep(self.TICK_LENGTH)

    def run(self):
        self.active = True

        self.bot.start()
        self.tick_thread = threading.Thread(target = self.tick)
        self.tick_thread.start()

        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(self.start_server())
        event_loop.run_forever()
    
    def stop(self, crashed=False):
        self.active = False
        self.exit_event.set()
        self.bot.stop(crashed=crashed)


if __name__ == "__main__":
    sim = Game()
    try:
        sim.run()
    except KeyboardInterrupt:
        sim.stop()
        raise
    except:
        sim.stop(crashed=True)
        raise
