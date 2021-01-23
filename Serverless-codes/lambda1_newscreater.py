import requests
import json
import datetime
import boto3


#this lambda grabs today's headlines, does sentiment analysis using AWS Comprehend
#and saves the news along with sentiment into a dynamodb table
def lambda_handler(event, context):
    findNews()
    return 'End of News Sentiment'


def findNews():
    #News from the newsapi.org
    #Fetch headlines using the API
    #IMPORTANT: Register in newsapi.org to get your own API key, it's super easy!
    response = requests.get("http://newsapi.org/v2/everything?q=bitcoin&from=2020-10-13&sortBy=publishedAt&apiKey=7eb4dcc8a9064a1f8be721792de1ee75")
    d=response.json()
    if (d['status']) == 'ok':
        for article in d['articles']:
            print(article['title'])
            newsTitle=article['title']
            timestamp=article['publishedAt']
            sentiment=json.loads(getSentiment(newsTitle))
            print(sentiment['Sentiment'])
            insertDynamo(sentiment['Sentiment'],newsTitle,timestamp)

#getSentiment function calls AWS Comprehend to get the sentiment
def getSentiment(newsTitle):
    comprehend = boto3.client(service_name='comprehend')
    return(json.dumps(comprehend.detect_sentiment(Text=newsTitle, LanguageCode='en'), sort_keys=True))

#inserts headline along with sentiment into Dynamo    
def insertDynamo(sentiment,newsTitle,timestamp):
    print("inside insert dynamo function")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Sentimented_News_Table')
    response = table.put_item(
       Item={
        'sentiment': sentiment,
        'title': newsTitle,
        'timestamp' : timestamp
       }
       )
       