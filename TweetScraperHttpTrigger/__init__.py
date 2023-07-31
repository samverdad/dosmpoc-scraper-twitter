import logging
import json
import os
from dotenv import load_dotenv
from datetime import datetime

import azure.functions as func
from azure.storage.blob import BlobServiceClient

from tweet_scraper import scrape_tweets


load_dotenv()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    ## Connect to the storage account
    connection_string = os.environ["AZ_SA_CONNECTION_STRING"]
    container_name = os.environ["AZ_SA_BLOB_CONTAINER_NAME"]
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    ## Convert tweets list to JSON
    tweets = scrape_tweets()
    tweets_json = json.dumps(tweets)

    ## Upload tweets to blob storage
    blob_name = f"output_tweets_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(tweets_json, overwrite=True)

    ## Return JSON
    return func.HttpResponse(tweets_json, mimetype='text/json')
