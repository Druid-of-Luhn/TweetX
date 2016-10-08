import operator
from collections import defaultdict

class VoteCounter(object):
    def __init__(self):
        self._votes = defaultdict(int)

    def tick(self):
        if self._votes.items():
            highest = max(self._votes.items(), key=operator.itemgetter(1))[0]
            self._votes = defaultdict(int)
            return highest

    def vote(self, move):
        print(move)
        self._votes[move] += 1
