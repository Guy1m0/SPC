# - *- coding: utf- 8 - *-
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import models
from dateutil import parser
from datetime import datetime
from tweepy.streaming import StreamListener

import json, sys, re, collections, math

access_token = "3028790692-6AeMsbCuaGZPDuV4MLWH3ymavgiBWFuGvZoVdbN"
access_token_secret = "Z0kBbO7OC7yC9Z9GJg3DQGYDJvOG5HWAj7XY70ZHPnNIT"
consumer_key = "nEHpCxgQjOLpfHXAAmlWzxwYF"
consumer_secret = "Sfa8e7tZPC4gDS2QYVQ3ykqMYHsC7gNhbaWtBTeXwMhbAbIAcO"

msg_filters_format = ["https://", "&"]
msg_filters_words = []
search_number = 5000

#use for streaming
class StdOutListener(StreamListener):
	count = 0
	hashtag = ''

	def __init__(self, hashtag, api):
		self.api = api
		self.hashtag = hashtag
		self.f = open(hashtag + '.txt', "w+")
		print self.hashtag

	def on_status(self, status):
		#print tag
		#print "running?"
		if (self.count < size):
			#f.write("original:" + status._json['text'].encode("utf-8") + "\n")
			text = takeout(status._json['text'])
			self.f.write(text + "\n")	
			#print status._json['text'].encode("utf-8")
			self.count = self.count + 1	
			print "count:", self.count
		else:
			self.f.close()
			sys.exit("Collect Finished")

	def on_error(self, status):
		print status

def takeout(msg, filters = msg_filters_format):
	msg = msg.encode("utf-8")
		#cut from the ':'
	index = msg.find(":")
	msg = msg[index + 1:]
	#print "original:", 	msg

	for char in filters:
		#print char
		buffer = ""
		for word in msg.split():
			if char not in word:
				buffer = buffer + word + " "

		msg = buffer

	msg = re.sub('[^a-zA-Z0-9\- ]+', '', msg)
	#print msg

	return msg[:-1]

def check_msg(msg, hashtag):
	#tag = hashtag
	#__set_up_dict(hashtag)
	msg = takeout(msg)
	__calculate_relevance(msg, hashtag)


def __set_up_dict(hashtag):
	f = open(hashtag + '.txt', "w+")

	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	
	api = tweepy.API(auth)

	search_text = hashtag
	search_result = []
	last_id = -1

	while len(search_result) < search_number:
		count = search_number - len(search_result)
		try:
			new_tweets = api.search(search_text, count = count, max_id = str(last_id -1))
			#print len(new_tweets)

			for msg in new_tweets:
				tweet = takeout(msg)
				#print msg
				search_result.append(tweet)
			if not new_tweets:
				break
			last_id = new_tweets[-1].id
		except tweepy.TweepError as e:
			break

	print "start to remove duplicate"
	result = list(set(search_result))
	print len(result)

	for msg in result:
		f.write(msg + "\n")

	f.close()
	sys.exit("collect finished")

	# use for the streaming
	'''
	listener = StdOutListener(hashtag, api)
	stream = Stream(auth, listener)

	#print hashtag
	stream.filter(track = ['#TrumpFirsts'])#[hashtag])
	'''

def __calculate_relevance(msg, hashtag):
	#f = open(hashtag + '.txt', "r")
	words = re.findall(r'\w+', open(hashtag + '.txt').read().lower())
	cnt = collections.Counter(words)	

	print cnt.most_common(30)

	cnt_tf = collections.Counter()
	cnt_idf = collections.Counter()
	cnt_tf_idf = collections.Counter()

	total = len(cnt)

	for word in list(cnt):
		line_count = 0
		with open (hashtag + '.txt') as f:
			for line in f:
				line_count += 1
				#print line
				for words in line.lower().split():
					if word == words:
						cnt_idf[word] += 1
						break

			if (cnt[word] == 0):

				cnt_tf_idf[word] = 0
				#break
			else:
				print "word:",word, cnt_idf[word], cnt[word]
				cnt_idf[word] = math.log10(float(line_count)/cnt_idf[word])
			#print word, cnt_idf[word]
			#print "tf:",cnt_tf[word],total
				cnt_tf[word] = float(cnt_tf[word])/total
			#print cnt_tf[word]
				cnt_tf_idf[word] = cnt_tf[word] * cnt_idf[word]
	sum = 0
	for word in msg.lower().split():
		print "%s tf_idf is: %f", word, cnt_tf_idf[word] 
		sum += cnt_tf_idf[word]

	print sum

if __name__ == '__main__':
	msg = "RT @crazylary51: #TrumpFirsts all the fuss Trump created about 1,000 jobs when @POTUS has created 16 million without bragging. https://t.c"
	check_msg(msg, '#TrumpFirsts')

	#msg = msg.encode("utf-8")
	#takeout(msg, ["https://","#", "@"])
	
	#print "running"

	


