import tweepy
from .vote import VoteCounter

from secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

voter = VoteCounter()

class ReplyListener(tweepy.StreamListener):
    def on_status(self, status):
        # TODO Stick these on a queue in future, so we don't fall behind.
        valid = voter.vote(status)

        if not valid:
            api.update_status("@{}: Sorry, it looks like that wasn't a valid command.".format(status.user.screen_name), in_reply_to_status_id=status.id)

    def on_error(self, status_code, msg="We got rate-limited, terminating!"):
        if status_code == 420:
            print(msg)
            return False

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

try:
    listener = ReplyListener()
    stream = tweepy.Stream(auth = api.auth, listener=listener)
    stream.filter(track=['@TweetX_Bot'])
except KeyboardInterrupt:
    pass
