from gtts import gTTS
from deep_translator import GoogleTranslator

def hindi_trans(text, output_filename="output.mp3"):
    # translate english text to hindi
    translated_text = GoogleTranslator(source="auto", target="hi").translate(text)

    # convert translated hindi text to speech
    tts = gTTS(text=translated_text, lang="hi")
    tts.save(output_filename)
    
    return output_filename
