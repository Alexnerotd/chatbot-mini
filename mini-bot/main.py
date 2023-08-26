import pyttsx3
import speech_recognition as sr
import json
import random

class Bot:
    def __init__(self):
        self.engine = pyttsx3.init()

    def talk(self, text):
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)

        try:
            if isinstance(text, str):
                voice = self.engine.say(text=text)
                self.engine.runAndWait()
                return voice
            else:
                print('El valor dado no es de tipo string')
        except ValueError as ve:
            print("Ocurrió un error antes de entrar al if ", ve)

    def hear(self):
        mic = sr.Microphone()
        rec = sr.Recognizer()

        with mic as source:
            listen = rec.listen(source)
            text = rec.recognize_google(listen)
            return text

    def load_json(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            return data

    def main(self):
        data_json = 'mini-bot/main.json'
        data = self.load_json(filename=data_json)
        text = self.hear().lower().strip()

        palabra = None

        for diccionario in data:
            for clave in diccionario:
                if text == clave.lower().strip():
                    palabra = random.choice(diccionario[clave])
                    break
            if palabra is not None:
                break

        if palabra is not None:
            self.talk(text=palabra)
        else:
            self.talk(text="Lo siento, no entendí lo que dijiste.")
            with open(data_json, 'r') as file:
                json_file = json.load(file)

                if isinstance(json_file, list) and json_file:
                    primer_dict = json_file[0]
                    if isinstance(primer_dict, dict):
                        primer_dict[text] = []

            with open(data_json, 'w') as file:
                json.dump(json_file, file, indent=4)

if __name__ == "__main__":
    bot = Bot()
    print("Escuchando...")
    bot.main()
