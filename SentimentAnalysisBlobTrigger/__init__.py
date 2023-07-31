import logging
import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv

import azure.functions as func
from azure.data.tables import TableClient
from azure.core.exceptions import ResourceExistsError

from .sentiment_analysis import sentiment_analysis


load_dotenv()

def main(myblob: func.InputStream):
    # Connect to Storage
    connection_string = os.environ["AZ_SA_CONNECTION_STRING"]
    table_name = "sentimentanalysis"
    table_client = TableClient.from_connection_string(conn_str=connection_string, table_name=table_name)

    try:
        table_client.create_table()
        logging.info("Created table")
    except ResourceExistsError:
        logging.warn("Table already exists")

    # Get blob from HTTP trigger function
    blob_content = myblob.read().decode('utf-8')
    blob_content_json = json.loads(blob_content)

    # Process data
    for data in blob_content_json:
        document = sentiment_analysis(data)

        if document is None:
            continue
        
        save_to_table(table_client, data, document)


def save_to_table(client, data, document):
    source_name = 'Twitter'
    subs = str(data['url']).split('/')
    row_key = subs[-1]
    timestamp = datetime.now()

    entity = {
        'PartitionKey': source_name,
        'RowKey': row_key,
        'Timestamp': timestamp,

        'Title': data['title'],
        'Author': data['author'],
        'DataPosted': data['datetime'],
        'Url': data['url'],
        'Content': data['content'],
        'Location': data['location'],
        'ReplyCount': data['replyCount'],
        'RetweetCount': data['retweetCount'],
        'LikeCount': data['likeCount'],
        'QuoteCount': data['quoteCount'],
        'ViewCount': data['viewCount'],
        'Lang': data['lang'],
        'InReplyToTweetId': data['inReplyToTweetId'],
        'InReplyToUser': data['inReplyToUser'],
        'MentionedUsers': ', '.join(data['mentionedUsers']),

        'Sentiment': document.sentiment,
        'PositiveSentimentConfidenceScore': document.confidence_scores.positive,
        'NeutralSentimentConfidenceScore': document.confidence_scores.neutral,
        'NegativeSentimentConfidenceScore': document.confidence_scores.negative,
    }

    client.upsert_entity(entity)
