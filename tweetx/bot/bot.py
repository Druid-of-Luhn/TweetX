import logging, time, tweepy
from .vote import Command, VoteCounter

from secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

BOT_NAME = 'TweetX_Bot'
log = logging.getLogger('tweetx')

class ReplyListener(tweepy.StreamListener):
        def __init__(self, voter, api):
            super().__init__()
            self._voter = voter
            self._api = api
            self.last_user = None

        def on_status(self, status):
            self.last_user = status.user.screen_name
            valid = self._voter.vote(status.text)

            if not valid:
                log.warning('Got an invalid Twitter command from @%s' % status.user.screen_name)
                self._api.update_status("@{}: Sorry, it looks like that wasn't a valid command.".format(status.user.screen_name), in_reply_to_status_id=status.id)

        def on_error(self, status_code):
            if status_code == 420:
                log.error("We got rate-limited, terminating!")
                return False

class TwitterBot():
    def __init__(self, game):
        self._game = game

        self._voter = VoteCounter(self)
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        self._api = tweepy.API(auth)

    def _current_time(self):
        return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())

    def start(self):
        self._api.update_status('TweetX went online @ {}'.format(self._current_time()))
        log.info('We\'re online!')

        self._listener = ReplyListener(self._voter, self._api)
        self._stream = tweepy.Stream(auth = self._api.auth, listener=self._listener)
        self._stream.filter(track=['@{}'.format(BOT_NAME)], async=True)

    def stop(self, crashed=False):
        self._api.update_status('TweetX went down @ {}.'.format(self._current_time()))
        self._stream.disconnect()

        if crashed and self._listener.last_user:
            self._api.update_status('Congratulations to @{} for breaking TweetX @ {}'.format(self._last_user, self._current_time()))

    def tick(self):
        command = self._voter.tick()

        spaceship = self._game.environment.spaceship

        command_map = {
            Command.FORWARD: spaceship.engine_on,
            Command.ENGINES_OFF: spaceship.engine_off,
            Command.LEFT: spaceship.turn_left,
            Command.RIGHT: spaceship.turn_right,
            Command.CHARGE_WEAPON: spaceship.charge_weapon,
            Command.FIRE_WEAPON: spaceship.fire_weapon,
            Command.RAISE_SHIELDS: spaceship.raise_shields,
            Command.LOWER_SHIELDS: spaceship.lower_shields,
            Command.DECHARGE_WEAPON: spaceship.decharge_weapon,
            Command.CHARGE_ENGINES: spaceship.charge_engine,
            Command.DECHARGE_ENGINES: spaceship.decharge_engine
        }

        try:
            command_map[command]()
        except KeyError:
            pass
