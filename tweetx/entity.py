#!/usr/bin/env python3

import logging
import math
import random
from enum import Enum

log = logging.getLogger('tweetx')

class Entity(object):
    def __init__(self, id, x, y, width, height):
        self.id = id
        self.x = x
        self.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.width = width
        self.height = height
        self.direction_orientation = 0

    def tick(self):
        pass

class Reactor():
    def __init__(self):
        self.power = 3

class PowerConsumer():
    def __init__(self, reactor):
        self.charge = 0
        self.reactor = reactor

    def increment_charge(self):
        if self.reactor.power > 0 and self.charge < 3:
            self.charge += 1
            self.reactor.power -= 1

    def is_charged(self):
        if self.charge >= 1:
            return True
        else:
            return False

    def reset(self):
        self.reactor.power += self.charge
        self.charge = 0

    def decrement_charge(self):
        if self.charge > 0:
            self.charge -= 1
            self.reactor.power += 1

class Weapon(PowerConsumer):
    pass

class Shield(PowerConsumer):
    pass

class EnginePower(PowerConsumer):
    pass

class Spaceship(Entity):
    WIDTH = 83
    HEIGHT = 76
    TURN_RADIANS = 0.785398
    FORCE = 100

    def __init__(self, environment, x, y):
        super().__init__('spaceship', x, y, self.WIDTH, self.HEIGHT)
        self.calculate_velocity_orientation()
        self.environment = environment
        self.direction_orientation = self.direction_velocity
        self.health = 6
        self.reactor = Reactor()
        self.weapon = Weapon(self.reactor)
        self.shield = Shield(self.reactor)
        self.engine_power = EnginePower(self.reactor)
        self.engine = False

    # counter clockwise
    def turn_left(self):
        self.direction_orientation += self.TURN_RADIANS

    # clockwise
    def turn_right(self):
        self.direction_orientation -= self.TURN_RADIANS

    def engine_on(self):
        self.engine = True

    def engine_off(self):
        self.engine = False

    def tick(self):
        if self.engine_on:
            force = self.FORCE*self.engine_power.charge
            self.velocity_x += force*math.cos(self.direction_orientation)
            self.velocity_y += force*math.sin(self.direction_orientation)
            self.calculate_velocity_orientation()

    def calculate_velocity_orientation(self):
        if self.velocity_y != 0:
            self.direction_velocity = math.atan(self.velocity_x/self.velocity_y)
        else:
            self.direction_velocity = 0

    def charge_weapon(self):
        self.weapon.increment_charge()

    def decharge_weapon(self):
        self.weapon.decrement_charge()

    def raise_shields(self):
        self.shield.increment_charge()

    def lower_shields(self):
        self.shield.decrement_charge()

    def fire_weapon(self):
        if self.weapon.is_charged():
            p = 0.25 * self.weapon.charge
            if random.uniform(0, 1) < p:
                enemies = sorted(self.environment.entities, key = lambda e: (e.x - self.x) ** 2 + (e.y - self.y) ** 2)
                for enemy in enemies:
                    if enemy != self:
                        self.environment.remove_entity(enemy)
                        log.info('Fired weapon and destroyed enemy %s' % enemy)
                        break
            else:
                log.info('Fired a weapon and failed')

            self.weapon.reset()

    def decrement_health(self):
        if not self.shield.is_charged():
            self.health -= 2
        else:
            self.health -= 1
            self.shield.decrement_charge()

    def charge_engine(self):
        self.engine_power.increment_charge()

    def decharge_engine(self):
        self.engine_power.decrement_charge()




class Meteor(Entity):
    def __init__(self, x, y):
        super().__init__('meteor%s' % (random.randrange(1000,30000) // 10**5), x, y, random.randrange(1,3), random.randrange(1,3))
        self.velocity_x = random.randrange(0,5)
        self.velocity_y = random.randrange(0,5)

class Planet(Entity):
    def __init__(self, x, y):
        radius = random.randrange(0, 10)
        super().__init__('planet%s' % (random.randrange(1000,30000) // 10**5), x, y, radius, radius)
