import speech_recognition as sr

class SpeechToText():
    def __init__(self):
        self.r = sr.Recognizer()

    def speech_to_text(self, audio):
        if not isinstance(audio, sr.AudioData):
            print("Dosya bir ses dosyası değil.")
            return
        
        try:
            return self.r.recognize_google(audio, language='tr-TR') # Ses dosyasını metne çevirme
        except sr.UnknownValueError:
            return "Anlaşılamayan ses."
        except sr.RequestError:
            return "Zaman aşımı"