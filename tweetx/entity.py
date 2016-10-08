#!/usr/bin/env python3

import math
import random
from enum import Enum

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

class Weapon():

    def __init__(self):
        self.charge = 0

    def increment_charge(self):
        if charge < 3:
            self.charge += 1

    def is_charged(self):
        if self.charge >= 1:
            return True
        else:
            return False

    def reset(self):
        self.charge = 0

class Shield():

    def __init__(self):
        self.charge = 0

    def increment_charge(self):
        if charge < 3:
            self.charge += 1

    def is_charged(self):
        if self.charge >= 1:
            return True
        else:
            return False

    def decrement_charge(self):
        self.charge -= 1
   
class Spaceship(Entity):
    WIDTH = 1
    HEIGHT = 1
    TURN_RADIANS = 0.785398
    FORCE = 5

    def __init__(self, x, y):
        super().__init__('spaceship', x, y, self.WIDTH, self.HEIGHT)
        self.calculate_velocity_orientation()
        self.direction_orientation = self.direction_velocity
        self.health = 6
        weapon = Weapon()
        shield = Shield()

    # counter clockwise
    def turn_left(self):
        self.direction_orientation += self.TURN_RADIANS

    # clockwise
    def turn_right(self):
        self.direction_orientation -= self.TURN_RADIANS

    def accelerate(self):
        self.velocity_x += self.FORCE*math.cos(self.direction_orientation)
        self.velocity_y += self.FORCE*math.sin(self.direction_orientation)
        self.calculate_velocity_orientation()

    def calculate_velocity_orientation(self):
        if self.velocity_y != 0:
            self.direction_velocity = math.atan(self.velocity_x/self.velocity_y)
        else:
            self.direction_velocity = 0

    def charge_weapon(self):
        weapon.increment_charge

    def fire_weapon(self):
        if weapon.is_charged():
            weapon.reset()

    def decrement_health(self):
        if not shield.is_charged():
            health -= 2
        else:
            health -= 1
            shield.decrement_charge()

class Meteor(Entity):
    
    def __init__(self, x, y):
        super().__init__('meteor', x, y,random.randrange(1,3),random.randrange(1,3))
        self.velocity_x = random.randrange(0,5)
        self.velocity_y = random.randrange(0,5)
