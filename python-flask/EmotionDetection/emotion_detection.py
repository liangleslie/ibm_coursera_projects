"""
This module provides a Flask-based web server for emotion detection.
It interfaces with the Watson NLP library to analyze text provided by users
via a web interface.
"""
from flask import Flask, render_template, request
# pylint: disable=import-error
from emotion_detection import emotion_detector

app = Flask(__name__)

@app.route("/emotionDetector")
def sent_analyzer():
    """
    Analyzes the text received from the frontend via a GET request.
    Returns a formatted string of emotion scores or an error message.
    """
    # Retrieve the text to analyze from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')

    # Pass the text to the emotion_detector function and store the response
    response = emotion_detector(text_to_analyze)

    # Extract the dominant emotion to check for None (error case)
    dominant_emotion = response['dominant_emotion']

    # Error handling for blank entries or invalid input
    if dominant_emotion is None:
        return "Invalid text! Please try again!"

    # Extract the individual emotions if the response is valid
    anger = response['anger']
    disgust = response['disgust']
    fear = response['fear']
    joy = response['joy']
    sadness = response['sadness']

    # Return the successful formatted string
    return (
        f"For the given statement, the system response is 'anger': {anger}, "
        f"'disgust': {disgust}, 'fear': {fear}, 'joy': {joy} and "
        f"'sadness': {sadness}. The dominant emotion is {dominant_emotion}."
    )

@app.route("/")
def render_index_page():
    """
    Renders the main application page (index.html).
    """
    return render_template('index.html')

if __name__ == "__main__":
    # Deploy the application on localhost:5000
    app.run(host="0.0.0.0", port=5000)