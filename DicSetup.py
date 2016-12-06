# - *- coding: utf- 8 - *-
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import models
from dateutil import parser
from datetime import datetime
from tweepy.streaming import StreamListener

import json, sys, re, collections, math, os

access_token = "3028790692-6AeMsbCuaGZPDuV4MLWH3ymavgiBWFuGvZoVdbN"
access_token_secret = "Z0kBbO7OC7yC9Z9GJg3DQGYDJvOG5HWAj7XY70ZHPnNIT"
consumer_key = "nEHpCxgQjOLpfHXAAmlWzxwYF"
consumer_secret = "Sfa8e7tZPC4gDS2QYVQ3ykqMYHsC7gNhbaWtBTeXwMhbAbIAcO"

msg_filters_format = ["https://", "&", "RT", "@"]
msg_filters_out = ["#Ad"]
msg_filters_words = ["https", "rt"]

cnt_tf = collections.Counter()
cnt_idf = collections.Counter()
cnt_tf_idf = collections.Counter()

level = []

search_number = 0

#use for streaming
class StdOutListener(StreamListener):
	num = 0
	hashtag = ''
	buffer = ""

	def __init__(self, hashtag, num, api):
		self.api = api
		self.hashtag = hashtag
		self.num = num
		#self.f = open(hashtag + '.txt', "w+")
		#print self.hashtag

	def on_status(self, status):
		f = open('steaming_result.txt', "w+")
		#print tag
		#print "running?"
		print "tweet:", status._json['text'].encode("utf-8")

		msg = status._json['text'].encode("utf-8")
		self.buffer += msg + "\n"
		self.buffer += "1 (Highest Risk) -----> 5 (Lowest Risk) \n"
		self.buffer += "This tweet risk is " + calculate_level(msg) + "\n"
		
		self.num -= 1

		if self.num == 0:
			f.write(self.buffer)
			f.close()
			sys.exit("streaming finished")
		f.close()
		#check_msg(msg, '#TrumpFirsts')

	def on_error(self, status):
		print status

def takeout(msg, filter_format = msg_filters_format, filter_words = msg_filters_words):
	#print "original:", 	msg
	msg = msg.lower()
	for char in filter_format:
		#print char
		buffer = ""
		for word in msg.split():
			#print "word:", word
			if char not in word:
				buffer = buffer + word + " "

		msg = buffer
	msg = msg[:-1]

	for words in filter_words:
		words = words.lower()
		#print char
		buffer = ""
		for word in msg.split():
			#print "word:", word
			if words != word:
				buffer = buffer + word + " "

		msg = buffer

	msg = re.sub('[^a-zA-Z0-9\-\# ]+', '', msg)

	return msg[:-1]

def calculate_level(msg):
	ssum = 0
	f = open('streaming_log.txt', "a+")
	#f.close()
	#f = open('streaming_log.txt', "a")
	print >> f, msg, "\n"
	msg = takeout(msg)

	filter_words = re.findall(r'\w+', open('frequency.txt').read().lower())

	print >> f, "---------------------------Analysis-------------------------------\n"
	for words in filter_words:
		buffer = ""
		for word in msg.lower().split():
			
			if words != word:
				buffer = buffer + word + " "

		msg = buffer

	msg = msg[:-1]

	for word in msg.lower().split():
		
		idf= float(search_number + 1)/(cnt_idf[word] + 1)
		print >> f, "word:", word, "inverse document frequcney:", idf, "\n"
		ssum += idf

	print >> f, "total value:", ssum, "effective words:", len(msg.split()), "\n"
	ssum = ssum/len(msg.split())
	print >> f, "risk value:", ssum, "\n"
	print >> f, "risk level break point:", level, "\n"

	for i in range(4):
		if ssum > level[i]:
			print >> f, "risk level:", i+1
			print >> f, "--------------------------------------------------------------"
			f.close()
			return str(i + 1)

	print >> f, "no risk"
	print >> f, "--------------------------------------------------------------"
	f.close()
	return str(5)

def __set_up_dict(hashtag):
	f = open(hashtag + '.txt', "w+")
	g = open(hashtag + '_bak.txt', "w+")

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
				msg = msg.text.encode("utf-8")

				#filter out any message contain rubbish
				for filter_item in msg_filters_out:
					if filter_item in msg.split():
						msg = ""

				if msg == "":
					break

				g.write("original:" + msg + "\n")
				tweet = takeout(msg)
				g.write("modified:" + tweet + "\n")
				f.write(tweet + "\n")
				#print msg
				search_result.append(tweet)
			if not new_tweets:
				break
			last_id = new_tweets[-1].id
		except tweepy.TweepError as e:
			break

	f.close()
	g.close()

def __update_relevance(hashtag):
	cnt = collections.Counter()	
	total = 0

	with open(hashtag + '.txt') as f:

		for word in f.read().split():
			#print "reading?"
			word = word.lower()
			#print word
			cnt[word] += 1
			total += 1
	f.close()

	#use frequency dictionary to filter out common words
	filter_words = re.findall(r'\w+', open('frequency.txt').read().lower())
	filter_words.append('https')
	for word in filter_words:
		del cnt[word]

	#total tweets in the database,
	num_tweet = cnt[hashtag.lower()]

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

			#cnt_idf[word] = math.log10(float(line_count)/cnt_idf[word])

			cnt_tf[word] = float(cnt[word])/total

	#print "test match", num_tweet, line_count

	f.close()

	#calculate the expectation level for the database
	tweet_level = []
	index = 0

	with open (hashtag + '.txt') as f:

		for line in f:

			ssum = 0
			for words in filter_words:
				buffer = ""
				for word in line.lower().split():
		
					if words != word:
						buffer = buffer + word + " "

				line = buffer

			line = line[:-1]
			if len(line) != 0:
				for word in line.lower().split():
		
					idf= float(search_number + 1)/(cnt_idf[word] + 1)
			#print "%s tf_idf is: %f", word, idf
				ssum += idf
				#print "line:", line, len(line)
				#print ssum, len(msg.split())
				ssum = ssum/len(line.split())

				tweet_level.append(ssum)
				index +=1
				ssum = 0

	f.close()
	#print "h", tweet_level
	tweet_level = sorted(tweet_level, key = float, reverse = True)
	
	level.append(tweet_level[int(search_number*0.001)])
	level.append(tweet_level[int(search_number*0.005)])
	level.append(tweet_level[int(search_number*0.02)])
	level.append(tweet_level[int(search_number*0.05)])
	#level.append(tweet_level[int(search_number*0.2)])

	print level


	#print cnt_tf_idf['of']
USAGE = """
usage: DicSetup <database size> <Hashtag> <mode> <parm>
       database size: the num of tweets collected from twitter
  	   mode: either 'streaming' or 'msg'
  	   parm: int number of the incoming tweets for mode 'streaming'
  	   		 or string for the mode 'msg'
       Default: 2000 '#Trump' streaming 5
       Running sample: python DicSetup.py 5000 NBA streaming 10
       			   or: python DicSetup.py 5000 NBA msg " rt XXX..."
       """


if __name__ == '__main__':

 	args = sys.argv[1:]

	if args == []:
		args.append(2000)
		args.append('#Trump')
		args.append("streaming")
		args.append(5)
	elif len(args) != 4:
		print "here?"
		sys.exit(USAGE)


	search_number = int(args[0])

	hashtag = args[1]
	hashtag = "#" + re.sub('[^a-zA-Z0-9]+', '', hashtag)

	msg_filters_words.append(hashtag)

	if not os.path.isfile(hashtag + '.txt'):
		__set_up_dict(hashtag)
		print "dict finished"

	__update_relevance(hashtag)
	
	if args[2] == "msg":

		msg = args[3]
		calculate_level(msg)
		#calculate_level(msg1)

	#check_msg(msg, '#TrumpFirsts')
	#check_msg(msg2, '#TrumpFirsts')
	elif args[2] == "streaming":
		num = int(args[3])
		
		auth = OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
	
		api = tweepy.API(auth)
		listener = StdOutListener(hashtag, num, api)
		stream = Stream(auth, listener)

	#print hashtag
		stream.filter(track = [hashtag])#[hashtag])
	else:
		sys.exit(USAGE)

	#print "running"

	


