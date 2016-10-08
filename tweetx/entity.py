#!/usr/bin/env python3

import math

class Entity(object):

    def __init__(self, id, x, y, width, height):
        self.id = id
        self.x = x
        self.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.width = width
        self.height = height

class Spaceship(Entity):
    WIDTH = 1
    HEIGHT = 1
    TURN_RADIANS = 0.174533
    FORCE = 1

    def __init__(self, x, y):
        super().__init__('spaceship', x, y, self.WIDTH, self.HEIGHT)
        calculate_velocity_orientation()
        self.direction_orientation = self.direction_velocity

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
