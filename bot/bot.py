import tweepy
from enum import Enum

from secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

class Command(Enum):
    TURN_LEFT = 1
    TURN_RIGHT = 2
    FORWARD = 3

class ReplyListener(tweepy.StreamListener):
    def _handle_command(text):
        return False

    def on_status(self, status):
        # Stick these on a queue in future.
        valid = self._handle_command(status.text)

        if not valid:
            api.update_status("@{}: Sorry, it looks like that wasn't a valid command.".format(status.user.screen_name), in_reply_to_status_id=status.id)

    def on_error(self, status_code):
        if status_code == 420:
            print ("We got rate-limited, terminating!")
            return False

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

listener = ReplyListener()
stream = tweepy.Stream(auth = api.auth, listener=listener)
stream.filter(track=['@TweetX_Bot'])
