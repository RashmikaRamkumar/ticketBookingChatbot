import io
import sounddevice as sd
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import numpy as np
import soundfile as sf

# Function to record Tamil audio and recognize speech
def record_tamil_audio():
    print("Recording... Speak now in Tamil!")
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            print("Recognizing... Please wait.")
            text = recognizer.recognize_google(audio, language="ta-IN")
            print(f"Recognized Tamil Text: {text}")
            return text
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Error with the recognition service: {e}")
        return None

# Function to translate Tamil text to English
def translate_tamil_to_english(tamil_text):
    try:
        translated = GoogleTranslator(source="ta", target="en").translate(tamil_text)
        return translated
    except Exception as e:
        print(f"Error during translation: {e}")
        return None

# Function to generate and play speech in Tamil
def speak_text_in_tamil(text):
    try:
        # Generate speech audio with gTTS
        tts = gTTS(text=text, lang="ta")
        # Save the generated audio to an in-memory file
        buffer = io.BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        # Load the audio data as raw PCM
        data, samplerate = sf.read(buffer, dtype='float32')
        # Play the audio
        sd.play(data, samplerate)
        sd.wait()  # Wait until the audio is finished playing
    except Exception as e:
        print(f"Error in generating or playing speech: {e}")

# Main function to handle Tamil voice input and translation
def main():
    print("Welcome to the Tamil Speech Assistant!")
    
    # Step 1: Capture Tamil speech input
    input_text = record_tamil_audio()
    
    if input_text:
        # Step 2: Translate the recognized Tamil text to English
        translated_to_english = translate_tamil_to_english(input_text)
        
        if translated_to_english:
            print(f"Translated to English: {translated_to_english}")
            
            # Prepare the response in English
            response_in_english = f" {translated_to_english} Thank you!"
            print(f"Response in English: {response_in_english}")
            
            # Translate the response back to Tamil
            response_in_tamil = translate_tamil_to_english(response_in_english)  # Reverse translation if needed
            if response_in_tamil:
                print(f"Translated Back to Tamil: {response_in_tamil}")
                # Step 3: Speak the response in Tamil
                speak_text_in_tamil(response_in_tamil)

if __name__ == "__main__":
    main()
