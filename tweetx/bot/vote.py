import operator

from enum import Enum
from fuzzywuzzy import process
from collections import defaultdict

REQUIRED_CERTAINTY = 60

class Command(Enum):
    FORWARD = 1
    LEFT = 2
    RIGHT = 3

CHOICES = {
    'forward': Command.FORWARD,
    'straight': Command.FORWARD,
    'onwards': Command.FORWARD,

    'left': Command.LEFT,
    'port': Command.LEFT,

    'right': Command.RIGHT,
    'starboard': Command.RIGHT
}

class VoteCounter(object):
    def __init__(self):
        self._votes = defaultdict(int)

    def tick(self):
        if self._votes.items():
            highest = max(self._votes.items(), key=operator.itemgetter(1))[0]
            self._votes = defaultdict(int)
            return highest

    def vote(self, string):
        move = self._parse_command(string)
        print(move)
        if move:
            self._votes[move] += 1
            return True

        return False

    def _parse_command(self, string):
        result, certainty = process.extractOne(string, CHOICES.keys())

        if certainty > REQUIRED_CERTAINTY:
            return CHOICES[result]
