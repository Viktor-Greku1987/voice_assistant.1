# библиотека для преобразования текста в аудио и его воспроизведение
import pyttsx3
# библиотека для снятия горлоса с микрофона и распознания
import speech_recognition

# инициализация интрументов распознания и ввода речи
recognizer = speech_recognition.Recognizer()
microphon = speech_recognition.Microphone()

# функция создает обект библиотеки pyttsx3 для воспроизведения ГОЛОСА , делает начальные настройки (из функции возвращщаем сам объект)
def init_engine():
    # созжаем объект для воспроизведения речи
    engin = pyttsx3.init('sapi5') # sapi5 - это настройки голосового движка от майкрасовт
    # из движка получаем все голоса
    voices = engin.getProperty('voices')
    for i in voices:
        print(i)

# функция распозания речи
def recognize_speech():
    with microphon:
        data = ''
        # регулировка окружаюещго шума
        recognizer.adjust_for_ambient_noise(microphon, duration = 2)
        try:
            print("скажите команду: ")
            # получим данные с миукрофона ввиде аудиопересменной
            audio = recognizer.listen(microphon, 5,5)
        except Exception as ex:
            print('ошибка : ', ex)
            return ''
        # распознание аудио онлайн через гугл
        data = recognizer.recognize_google(audio, language= 'ru')
        return data


print('вы сказади:', recognize_speech())
#init_engine()

