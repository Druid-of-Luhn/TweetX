import tweepy
from enum import Enum
from vote import VoteCounter

from secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

class Command(Enum):
    TURN_LEFT = 1
    TURN_RIGHT = 2
    FORWARD = 3

voter = VoteCounter()

class ReplyListener(tweepy.StreamListener):
    def _handle_command(self, text):
        if 'TURN_LEFT' in text:
            voter.vote(Command.TURN_LEFT)
            return True
        elif 'TURN_RIGHT' in text:
            voter.vote(Command.TURN_RIGHT)
            return True
        elif 'FORWARD' in text:
            voter.vote(Command.FORWARD)
            return True

        return False

    def on_status(self, status):
        # TODO Stick these on a queue in future, so we don't fall behind.
        valid = self._handle_command(status.text)

        if not valid:
            api.update_status("@{}: Sorry, it looks like that wasn't a valid command.".format(status.user.screen_name), in_reply_to_status_id=status.id)

    def on_error(self, status_code, msg="We got rate-limited, terminating!"):
        if status_code == 420:
            print(msg)
            return False

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

listener = ReplyListener()
stream = tweepy.Stream(auth = api.auth, listener=listener)
stream.filter(track=['@TweetX_Bot'])
