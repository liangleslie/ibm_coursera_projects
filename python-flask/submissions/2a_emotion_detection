import requests
import json

def emotion_detector(text_to_analyze):
    """
    Analyzes the emotion of a given text using Watson NLP Emotion Predict service.
    
    Args:
        text_to_analyze (str): The string of text to be analyzed.
        
    Returns:
        str: The text attribute of the response from the API.
    """
    # Define the URL for the Emotion Predict service
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    
    # Define the headers required for the API request
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    
    # Define the input JSON payload
    input_json = { "raw_document": { "text": text_to_analyze } }
    
    # Send the POST request to the service
    response = requests.post(url, json=input_json, headers=headers)
    
    # Return the text attribute of the response object
    return response.text