from keys import *
import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob

class TwitterClient:

	def __init__(self):
		try: 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			self.auth.set_access_token(access_token, access_token_secret) 
			self.api = tweepy.API(self.auth)
 
		except: 
			print("Error: Authentication Failed")

	def get_tweet_sentiment(self, tweet): 
		analysis = TextBlob(self.clean_tweet(tweet))
		return analysis.sentiment.polarity
			
	def clean_tweet(self, tweet): 
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\/\/\S+)", " ", tweet).split())
		
	def get_user_tweets(self, query, count = 20): 		
		try: 
			fetched_tweets = self.api.user_timeline(id = query, count = count) 
			return self.parse_tweet_text(fetched_tweets)
		except tweepy.TweepError as e:
			try: 
				# print error (if any) 
				fetched_tweets = self.api.user_timeline(id = query, count = count) 
				return self.parse_tweet_text(fetched_tweets)
			except:
				raise ValueError("wrong username")	

	def get_viral_tweets(self, query, count = 50):
		try:
			fetched_tweets = self.api.search(q = query, count = count, result_type='popular')
			return self.parse_tweet_text(fetched_tweets)
		except tweepy.TweepError:
			try: 
				# print error (if any) 
				fetched_tweets = self.api.search(q = query, count = count, result_type='popular')
				return self.parse_tweet_text(fetched_tweets)
			except:
				raise ValueError("bad search")

	def parse_tweet_text(self, tweetArr):
		tweets = []
		for tweet in tweetArr:
			parsed_tweet = {}
			parsed_tweet['text'] = tweet.text
			parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
			parsed_tweet['rt_count'] = tweet.retweet_count
			if tweet.retweet_count > 0: 
					# if tweet has retweets, ensure that it is appended only once 
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
			else: 
				tweets.append(parsed_tweet)
		return tweets            



