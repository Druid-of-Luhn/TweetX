import time, tweepy
from .vote import Command, VoteCounter

from secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

BOT_NAME = 'TweetX_Bot'

class ReplyListener(tweepy.StreamListener):
        def __init__(self, voter, api):
            super().__init__()
            self._voter = voter
            self._api = api
            self._last_user = None

        def on_status(self, status):
            self._last_user = status.user.screen_name
            valid = self._voter.vote(status.text)

            if not valid:
                self._api.update_status("@{}: Sorry, it looks like that wasn't a valid command.".format(status.user.screen_name), in_reply_to_status_id=status.id)

        def on_error(self, status_code):
            if status_code == 420:
                print("We got rate-limited, terminating!")
                return False

class TwitterBot():
    def __init__(self, game):
        self._game = game

        self._voter = VoteCounter()
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        self._api = tweepy.API(auth)

    def _current_time(self):
        return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())

    def start(self):
        self._api.update_status('TweetX went online @ {}'.format(self._current_time()))

        listener = ReplyListener(self._voter, self._api)
        self._stream = tweepy.Stream(auth = self._api.auth, listener=listener)
        self._stream.filter(track=['@{}'.format(BOT_NAME)], async=True)

    def stop(self, crashed=False):
        self._api.update_status('TweetX went down @ {}.'.format(self._current_time()))
        self._stream.disconnect()

        if crashed and self._last_user:
            self._api.update_status('Congratulations to @{} for breaking TweetX @ {}'.format(self._last_user, self._current_time()))

    def tick(self):
        command = self._voter.tick()

        command_map = {
            Command.FORWARD: self._game.environment.spaceship.accelerate(),
            Command.LEFT: self._game.environment.spaceship.turn_left(),
            Command.RIGHT: self._game.environment.spaceship.turn_right()
        }

        if command:
            command_map[command]()
