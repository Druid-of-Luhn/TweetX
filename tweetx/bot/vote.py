import logging, operator

from enum import Enum
from collections import defaultdict

REQUIRED_CERTAINTY = 60
log = logging.getLogger('tweetx')

class Command(Enum):
    FORWARD = 1
    LEFT = 2
    RIGHT = 3

    CHARGE_WEAPON = 4
    FIRE_WEAPON = 5
    RAISE_SHIELDS = 6
    LOWER_SHIELDS = 7

SINGLE_MOVES = {
    'forwards': Command.FORWARD
    'forward': Command.FORWARD
    'straight': Command.FORWARD
    'onwards': Command.FORWARD

    'left': Command.LEFT
    'port': Command.LEFT

    'right': Command.RIGHT,
    'starboard': Command.RIGHT

    'charge': Command.CHARGE_WEAPON
    'fire': Command.FIRE_WEAPON
    'raise': Command.RAISE_SHIELDS
    'lower': Command.LOWER_SHIELDS
}

class VoteCounter():
    def __init__(self, bot):
        self._votes = defaultdict(int)
        self._bot = bot

    def _parse_command(self, string):
        lower_string = string.lower()
        
        words = lower_string.split()

        for word in words:
            try:
                choice = SINGLE_MOVES[word]
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
            log.info('Got a vote for %s' % move)
            self._votes[move] += 1
            self._bot.tick()
            return True

        self._bot.tick()
        return False
