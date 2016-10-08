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

class Weapon():

    def __init__(self, position):
        self.position = position
        self.charge = 0

    def increment_charge(self):
        self.charge += 25

    def is_charged(self):
        if self.charge == 100:
            return True
        else:
            return False

    def reset(self):
        self.charge = 0
   
class Spaceship(Entity):
    WIDTH = 1
    HEIGHT = 1
    TURN_RADIANS = 0.174533
    FORCE = 1

    def __init__(self, x, y):
        super().__init__('spaceship', x, y, self.WIDTH, self.HEIGHT)
        calculate_velocity_orientation()
        self.direction_orientation = self.direction_velocity
        self.ammo = 15
        self.health = 5
        weapons = [Weapon('top'), Weapon('bottom'), Weapon('front'), Weapon('back')]

    # counter clockwise
    def turn_left():
        self.direction_orientation += TURN_RADIANS

    # clockwise
    def turn_right():
        self.direction_orientation -= TURN_RADIANS

    def accelerate():
        self.velocity_x += FORCE*math.cos(self.direction_orientation)
        self.velocity_y += FORCE*math.sin(self.direction_orientation)
        calculate_velocity_orientation()

    def calculate_velocity_orientation:
        if self.velocity_y != 0:
            self.direction_velocity = math.atan(self.velocity_x/self.velocity_y)
        else:
            self.direction_velocity = 0

    def charge_weapon(self, position):
        for weapon in weapons:
            if weapon.position == position:
                weapon.increment_charge

    def fire_weapon(self, position):
        for weapon in weapons:
            if weapon.position == position:
                if weapon.is_charged():
                    weapon.reset()
                    ammo -= 1

class Meteor(Entity):
    
    def __init__(self, x, y):
        super().__init__('meteor', x, y,random.randrange(1,3),random.randrange(1,3))
        self.velocity_x = random.randrange(0,5)
        self.velocity_y = random.randrange(0,5)
