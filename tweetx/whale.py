# Random entities for testing

import random
from entity import Entity

class Dolphin(Entity):

    def __init__(self, id, x, y):
        super().__init__(id, x, y, 2, 1)
        self.velocity_x = random.uniform(0, 1)
        self.velocity_y = random.uniform(0, 1)


class SeaHorse(Entity):

    def __init__(self, id, x, y):
        super().__init__(id, x, y, 1, 2)
        self.velocity_x = random.uniform(0, 1)
        self.velocity_y = random.uniform(0, 1)
