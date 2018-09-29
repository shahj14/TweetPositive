from flask import Flask
from flask_restful import Resource, Api
from analysis import TwitterClient

app = Flask(__name__)
api = Api(app)

twitterApi = TwitterClient()

class Tweets(Resource):
	def get(self, search):
		tweets = twitterApi.get_tweets(search)
		return {
			"score" : sum([tweet['sentiment'] for tweet in tweets]),
			"happy_tweets": sum([1 for i in tweets if i['sentiment'] > 0]),
			"sad_tweets": sum([1 for i in tweets if i['sentiment'] < 0]),
			"tweets": tweets
		}

api.add_resource(Tweets, '/user/<string:search>')

if __name__ == '__main__':
	app.run(debug=True)