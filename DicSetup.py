import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import models
from dateutil import parser
from datetime import datetime
from tweepy.streaming import StreamListener

import json

access_token = "3028790692-6AeMsbCuaGZPDuV4MLWH3ymavgiBWFuGvZoVdbN"
access_token_secret = "Z0kBbO7OC7yC9Z9GJg3DQGYDJvOG5HWAj7XY70ZHPnNIT"
consumer_key = "nEHpCxgQjOLpfHXAAmlWzxwYF"
consumer_secret = "Sfa8e7tZPC4gDS2QYVQ3ykqMYHsC7gNhbaWtBTeXwMhbAbIAcO"


class StdOutListener(StreamListener):
	


	def on_data(self, data):
		print data
		return True


	def on_error(self, status):
		print status



if __name__ == '__main__':

	print "running"
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)

	stream.filter(track = ['python', 'javascript', 'ruby'])

