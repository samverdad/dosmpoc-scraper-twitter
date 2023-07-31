import os
from dotenv import load_dotenv

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


load_dotenv()

def sentiment_analysis(data):
    # Connect to Cognitive Services
    ta_credential = AzureKeyCredential(os.environ['AZ_CS_LANGUAGE_KEY'])
    text_analytics_client = TextAnalyticsClient(endpoint=os.environ['AZ_CS_LANGUAGE_ENDPOINT'], credential=ta_credential)

    content = [''.join(data['content'])]
    response = text_analytics_client.analyze_sentiment(content, show_opinion_mining=True)
    documents = [doc for doc in response if not doc.is_error]
    
    try:
        document = documents[0]
    except IndexError:
        document = None

    return document
