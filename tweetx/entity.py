#!/usr/bin/env python3

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

    def __init__(self, x, y):
        super().__init__('spaceship', x, y, self.WIDTH, self.HEIGHT)
