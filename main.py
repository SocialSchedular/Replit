from flask import Flask, request, render_template
import tweepy
import os

app = Flask(__name__)

# Authenticate with X/Twitter API
auth = tweepy.OAuth1UserHandler(
    os.environ['SAEih6uqaYuyZv3DD97yfo6E7'],
    os.environ['IdCSntBPW6eGrEspCi0hm9xGk5oG24naVgGEsXXfYGXwZcicCfT'],
    os.environ['1748742978468753408-EfrbHBlRO811kZhRayRwIJUumMYxxT'],
    os.environ['Clq1aBCVZbsg0aJXyUOvNNPBRWF6XlkHmvyFawzejwbkg']
)
api = tweepy.API(auth)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tweet', methods=['POST'])
def tweet():
    content = request.form['tweet_content']
    try:
        api.update_status(content)
        return 'Tweet posted!'
    except Exception as e:
        return f'Error: {e}'

