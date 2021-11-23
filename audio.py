import speech_recognition as sr
from vosk import Model, KaldiRecognizer 
import wave 
import json 


def recognize_audio(model='google'):
    # инициализация инструментов распознавания и ввода речи
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone:
        # регулирование уровня окружающего шума
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Слушаю...")
            #recognizer.energy_threshold = 300
            #recognizer.pause_threshold = 3
            audio = recognizer.listen(microphone)

        except sr.WaitTimeoutError:
            print("Проверьте ваш микрофон.")
            return

    # распознаем с помощью google api 
    if model == 'google':
        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
        except:
            text = 'Не удалось распознать. Попробуйте еще раз. После нажатия на кнопку подождите 3-4 секунды.'


    # если google не отвечает, используем офлайн библиотеку vosk
    elif model == 'vosk':
        with open("microphone-results.wav", "wb") as file:
            file.write(audio.get_wav_data())

        # анализ записанного в микрофон аудио
        wave_audio_file = wave.open("microphone-results.wav", "rb")

        model = Model("models/vosk-model-small-ru-0.4")
        offline_recognizer = KaldiRecognizer(model, wave_audio_file.getframerate())
        data = wave_audio_file.readframes(wave_audio_file.getnframes())

        if len(data) > 0:
            if offline_recognizer.AcceptWaveform(data):
                text = offline_recognizer.Result()
                # получение данных распознанного текста из JSON-строки
                text = json.loads(text)
                text = text["text"]
            else:
                text = offline_recognizer.PartialResult()
                text = json.loads(text)
                text = text["partial"]

    return text


if __name__ == "__main__":
    text = recognize_audio()
    print(text)