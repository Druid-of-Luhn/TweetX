# Random entities for testing

import random
from entity import Entity

class Dolphin(Entity):

    def __init__(self, x, y):
        super().__init__('dolphin%d' % (random.randrange(1000,90000)), x, y, 121, 81)
        self.velocity_x = random.uniform(0, 1) * 500
        self.velocity_y = random.uniform(0, 1) * 500


class SeaHorse(Entity):

    def __init__(self, id, x, y):
        super().__init__('seahorse%d' % (id(self) // 10**5), x, y, 1, 2)
        self.velocity_x = random.uniform(0, 1) 
        self.velocity_y = random.uniform(0, 1)
