# Random entities for testing

from entity import Entity

public class Dolphin(Entity):

    def __init__(self, x, y):
        super().__init__(x, y, 2, 1)


public class SeaHorse(Entity):

    def __init__(self, x, y):
        super().__init__(x, y, 1, 2)
