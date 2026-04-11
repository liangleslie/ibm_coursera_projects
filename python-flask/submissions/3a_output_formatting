import requests
import json

def emotion_detector(text_to_analyze):
    """
    Analyzes text and returns a dictionary of emotion scores and the dominant emotion.
    """
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }
    
    response = requests.post(url, json=input_json, headers=headers)
    
    # Convert the response text into a dictionary
    formatted_response = json.loads(response.text)
    
    # Extract the emotion scores from the nested dictionary structure
    # Path: emotionPredictions -> [0] -> emotion
    emotions = formatted_response['emotionPredictions'][0]['emotion']
    
    anger_score = emotions['anger']
    disgust_score = emotions['disgust']
    fear_score = emotions['fear']
    joy_score = emotions['joy']
    sadness_score = emotions['sadness']
    
    # Define the set of emotions to compare for the dominant emotion
    emotion_list = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score
    }
    
    # Logic to find the dominant emotion (the key with the highest value)
    dominant_emotion = max(emotion_list, key=emotion_list.get)
    
    # Construct the final output format
    result = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score,
        'dominant_emotion': dominant_emotion
    }
    
    return result