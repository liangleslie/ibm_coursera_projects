import unittest
from emotion_detection import emotion_detector

class TestEmotionDetector(unittest.TestCase):
    
    def test_joy(self):
        print("\nTesting: 'I am glad this happened'...")
        result = emotion_detector('I am glad this happened')
        self.assertEqual(result['dominant_emotion'], 'joy')
        print(f"Status: SUCCESS. Dominant emotion detected: {result['dominant_emotion']}")

    def test_anger(self):
        print("\nTesting: 'I am really mad about this'...")
        result = emotion_detector('I am really mad about this')
        self.assertEqual(result['dominant_emotion'], 'anger')
        print(f"Status: SUCCESS. Dominant emotion detected: {result['dominant_emotion']}")

    def test_disgust(self):
        print("\nTesting: 'I feel disgusted just hearing about this'...")
        result = emotion_detector('I feel disgusted just hearing about this')
        self.assertEqual(result['dominant_emotion'], 'disgust')
        print(f"Status: SUCCESS. Dominant emotion detected: {result['dominant_emotion']}")

    def test_sadness(self):
        print("\nTesting: 'I am so sad about this'...")
        result = emotion_detector('I am so sad about this')
        self.assertEqual(result['dominant_emotion'], 'sadness')
        print(f"Status: SUCCESS. Dominant emotion detected: {result['dominant_emotion']}")

    def test_fear(self):
        print("\nTesting: 'I am really afraid that this will happen'...")
        result = emotion_detector('I am really afraid that this will happen')
        self.assertEqual(result['dominant_emotion'], 'fear')
        print(f"Status: SUCCESS. Dominant emotion detected: {result['dominant_emotion']}")

if __name__ == '__main__':
    # Using verbosity=2 provides more detail in the standard unittest output
    unittest.main(verbosity=2)