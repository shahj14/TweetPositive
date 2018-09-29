from flask import Flask
from flask_restful import Resource, Api
from analysis import TwitterClient

app = Flask(__name__)
api = Api(app)

twitterApi = TwitterClient()

class UserTweets(Resource):
	def get(self, search):
		tweets = twitterApi.get_user_tweets(search)
		return {
			"score" : sum([tweet['sentiment'] for tweet in tweets]),
			"happy_tweets": sum([1 for i in tweets if i['sentiment'] > 0]),
			"sad_tweets": sum([1 for i in tweets if i['sentiment'] < 0]),
			"tweets": tweets
		}

class TrendTweets(Resource):
	def get(self, search):
		tweets = twitterApi.get_viral_tweets(search)
		return {
			"score" : sum([tweet['sentiment'] for tweet in tweets]),
			"happy_tweets": sum([1 for i in tweets if i['sentiment'] > 0]),
			"sad_tweets": sum([1 for i in tweets if i['sentiment'] < 0]),
			"tweets": tweets
		}		

class GeoTweets(Resource):
	def get(self, search):
		return {"feature": "coming soon"}


api.add_resource(UserTweets, '/user/<string:search>')
api.add_resource(GeoTweets, '/geo/<string:search>')
api.add_resource(TrendTweets, '/trend/<string:search>')

if __name__ == '__main__':
	app.run(debug=True)