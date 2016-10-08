import operator

from enum import Enum
from collections import defaultdict

REQUIRED_CERTAINTY = 60

class Command(Enum):
    FORWARD = 1
    LEFT = 2
    RIGHT = 3
    CHARGE_TOP = 4
    CHARGE_LEFT = 5
    CHARGE_RIGHT = 6
    CHARGE_BOTTOM = 7

MOVE_CHOICES = {
    'forwards': Command.FORWARD,
    'forward': Command.FORWARD,
    'straight': Command.FORWARD,
    'onwards': Command.FORWARD,

    'left': Command.LEFT,
    'port': Command.LEFT,

    'right': Command.RIGHT,
    'starboard': Command.RIGHT
}

class VoteCounter():
    def __init__(self):
        self._votes = defaultdict(int)

    def _parse_command(self, string):
        lower_string = string.lower()
        
        if 'charge' in lower_string:
            if 'front' in lower_string:
                return Command.CHARGE_TOP
            elif 'left' in lower_string:
                return Command.CHARGE_LEFT
            elif 'right' in lower_string:
                return Command.CHARGE_RIGHT
            elif 'back' in lower_string:
                return Command.CHARGE_BOTTOM
        elif 'fire' in lower_string:
            pass  # TODO implement
        else:
            words = lower_string.split()

        for word in words:
            try:
                choice = MOVE_CHOICES[word]
                return choice
            except KeyError:
                pass

    def tick(self):
        if self._votes.items():
            highest = max(self._votes.items(), key=operator.itemgetter(1))[0]
            self._votes = defaultdict(int)
            return highest

    def vote(self, string):
        move = self._parse_command(string)
        if move:
            self._votes[move] += 1
            return True

        return False
