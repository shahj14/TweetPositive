from flask import Flask, render_template
from flask_restful import Resource, Api
from analysis import TwitterClient
import requests

app = Flask(__name__)
api = Api(app)

twitterApi = TwitterClient()

@app.route('/')
def index():
	r = requests.get('http://localhost:5000/user/jeetshahuc')
	return render_template('index.html', tweets=r.json())

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

api.add_resource(UserTweets, '/user/<string:search>')
api.add_resource(TrendTweets, '/trend/<string:search>')

if __name__ == '__main__':
	app.run(debug=True)