

class Entity(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.width = width
        self.height = height
