from vosk import Model, KaldiRecognizer  # оффлайн-распознавание
import pyttsx3  # синтез речи
import speech_recognition  # распознавание речи
import random
import wave  # создание и чтение формата wav
import json
import os
from termcolor import colored


class Translation():
    with open('translation.json', 'r', encoding="UTF-8") as file:
        translations = json.load(file)

    def get(self, text: str):
        if text in self.translations:
            return self.translations[text][assistant.speech_language]
        else:
            print(colored("Not translated pharse: {}".format(text), 'red'))


class Person():
    '''
    Имя пользователя, город(ну это чтобы юзать для погоды), родной язык
    '''
    name = ''
    home_sity = ''
    native_language = ''


class VoiceAssistant:
    '''
    Имя, пол и язык речи ассистента
    '''
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""


def setup_asssistant_voice():
    """
    Установка голоса по умолчанию
    """
    voices = engine.getProperty('voices')

    if assistant.speech_language == "en":
        assistant.recognition_language = "en-US"
        if assistant.sex == "female":
            # Microsoft Zira Desktop - English (United States)
            engine.setProperty("voice", voices[1].id)
        else:
            # Microsoft David Desktop - English (United States)
            engine.setProperty("voice", voices[2].id)
    else:
        assistant.recognition_language = "ru-RU"
        # Microsoft Irina Desktop - Russian
        engine.setProperty("voice", voices[0].id)


def record_and_recognize_audio(*args: tuple):
    with microphone:
        recognized_data = ""

        # регулирование уровня окружающего шума
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 5, 5)

            with open("microphone-results.wav", "wb") as file:
                file.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return

        # использование online-распознавания через Google
        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()

        except speech_recognition.UnknownValueError:
            pass

        # в случае проблем с доступом в Интернет происходит попытка
        # использовать offline-распознавание через Vosk
        except speech_recognition.RequestError:
            print("Trying to use offline recognition...")
            # recognized_data = use_offline_recognition()

        return recognized_data


'''
В разработке 
def use_offline_recognition():
    """
    Переключение на оффлайн-распознавание речи
    :return: распознанная фраза
    """
    recognized_data = ""
    try:
        # проверка наличия модели на нужном языке в каталоге приложения
        if not os.path.exists("models/vosk-model-small-ru-0.4"):
            print("Please download the model from:\n"
                  "https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
            exit(1)

        # анализ записанного в микрофон аудио (чтобы избежать повторов фразы)
        wave_audio_file = wave.open("microphone-results.wav", "rb")
        model = Model("models/vosk-model-small-ru-0.4")
        offline_recognizer = KaldiRecognizer(model, wave_audio_file.getframerate())

        data = wave_audio_file.readframes(wave_audio_file.getnframes())
        if len(data) > 0:
            if offline_recognizer.AcceptWaveform(data):
                recognized_data = offline_recognizer.Result()

                # получение данных распознанного текста из JSON-строки
                # (чтобы можно было выдать по ней ответ)
                recognized_data = json.loads(recognized_data)
                recognized_data = recognized_data["text"]
    except:
        print("Sorry, speech service is unavailable. Try again later")

    return recognized_data
'''


def play_voice_assistant_speech(text_to_speach):
    engine.say(str(text_to_speach))
    engine.runAndWait()


def hello(*args,tuple):
    hello = [
        translator.get("Hello, {}, How can I help you today?").format(person.name),
        translator.get("Good day to you {}! How can I help you?").format(person.name)
    ]
    play_voice_assistant_speech(hello[random.randint(0, len(hello) - 1)])

def execute_command_with_name(command_name: str, *args: list):
    for key in commands.keys():
        if command_name in key:
            commands[key](*args)
        else:
            print("Command not found((")


commands = {
    ("hello", "привет"): hello
}

if __name__ == "__main__":

    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    engine = pyttsx3.init()

    assistant = VoiceAssistant()
    assistant.name = "Mila"
    assistant.sex = 'female'
    assistant.speech_language = 'ru'

    person = Person()
    person.name = "Mikhail"

    setup_asssistant_voice()

    translator = Translation()

    while True:
        voice_input = record_and_recognize_audio()
        os.remove("microphone-results.wav")
        print(voice_input)

        a = voice_input.split(" ")     
        command = voice_input[0]
        command_option = [str(input_part) for input_part in a[1:len(a)]]
        execute_command_with_name(command, command_option)
