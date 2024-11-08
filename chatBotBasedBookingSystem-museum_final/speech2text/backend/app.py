from flask import Flask, jsonify
from flask_cors import CORS  # To handle CORS issues
import speech_recognition as sr

# Initialize recognizer and Flask app
r = sr.Recognizer()
app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/voice', methods=['GET'])
def get_voice_input():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            print("Listening...")
            audio = r.listen(source)
            MyText = r.recognize_google(audio).lower()
            print(f"Recognized: {MyText}")
            return jsonify({"text": MyText})

    except sr.RequestError as e:
        return jsonify({"error": f"API request error: {str(e)}"}), 500

    except sr.UnknownValueError:
        return jsonify({"error": "Unable to recognize speech"}), 400
if __name__ == "__main__":
    app.run(host="localhost", port=5001)
