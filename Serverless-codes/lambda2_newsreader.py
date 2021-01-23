import json
import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb')



def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):
    table = dynamodb.Table('Sentimented_News_Table')
    operation = event['httpMethod']
    if operation =='POST' or 'GET':
        inputSentiment= event['queryStringParameters'].values()
        print(inputSentiment)
        try:
            # Querying the table using Primary key
            response = table.query(
                KeyConditionExpression=Key('sentiment').eq(''.join(inputSentiment)),
                Limit=10, #limits returned news to 10
                ScanIndexForward=False) #descending order of timestamp, most recent news first
        
            return respond(None, response)
         #return response
        except:
            raise
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
       
       
    
