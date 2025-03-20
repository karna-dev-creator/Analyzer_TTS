import os
import hashlib
from gtts import gTTS
from deep_translator import GoogleTranslator

def hindi_trans(text):
    """ Convert text to Hindi speech and save it as a unique audio file. """
    
    # Translate English text to Hindi
    translated_text = GoogleTranslator(source="auto", target="hi").translate(text)

    # Generate a unique filename using a hash of the text
    filename = f"tts_{hashlib.md5(text.encode()).hexdigest()}.mp3"
    filepath = os.path.join("audio", filename)

    # Ensure the "audio" folder exists
    os.makedirs("audio", exist_ok=True)

    # Check if the file already exists (avoid redundant conversions)
    if not os.path.exists(filepath):
        tts = gTTS(text=translated_text, lang="hi")
        tts.save(filepath)

    return filename  # Return the filename to be played in Streamlit
