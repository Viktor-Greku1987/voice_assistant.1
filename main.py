# библиотека для преобразования текста в аудио и его воспроизведение
import pyttsx3
# библиотека для снятия горлоса с микрофона и распознания
import speech_recognition
import time
import random
import requests
import os
import psutil
import requests
from bs4 import BeautifulSoup
import webbrowser
from datetime import datetime
import time
import os
import threading
from googletrans import Translator


def shutdown_PK(text = str, waiting_time=100):
    minuta = 0
    key_value = {"key_value": ['выключи', 'выключение']}
    text = text.split()
    if text != key_value:
        return ''
    while minuta < waiting_time:
        time.sleep(60)
        minuta += 1
    os.system('shutdown -s')
    potok = threading.Thread(target=shutdown_PK, args=waiting_time)
    return potok.start()

answer = ''

# список для хранения найденых файлов при выполнения функции поиска файлов
list_file = list()

# инициализация интрументов распознания и ввода речи
recognizer = speech_recognition.Recognizer()
microphon = speech_recognition.Microphone()

# функция создает обект библиотеки pyttsx3 для воспроизведения ГОЛОСА , делает начальные настройки (из функции возвращщаем сам объект)
def init_engine():
    # созжаем объект для воспроизведения речи
    engin = pyttsx3.init('sapi5') # sapi5 - это настройки голосового движка от майкрасовт
    # из движка получаем все голоса
    voices = engin.getProperty('voices')
    """
    for i in voices:
        print(i)
    """
    # настраиваем голос на русский женский Татьяна
    engin.setProperty('voice', voices[0].id)
    # настроим громкость воспроизведения
    # volume = engin.getProperty('volume')
    # print(volume)
    engin.setProperty('volume', 0.8)
    # настройка скорости воспроизведения звука
    rate = engin.getProperty('rate')
    print(rate)
    engin.setProperty('rate', 185)
    #help(engin)
    return engin
# функция озвучки нужного тектса на вход принимает два параметра: настоенный голос и текст , который нужнго озвучить
def sound(engin, text):
    # вызываем функцию синтеза тектста в речь
    engin.say(text)
    # воспроизводим полученное аудио
    engin.runAndWait()

# ф-ция на наличе приветввия или прощания
def hi_goodby(text):
    global answer
    first_greeting = ['вижу вас как на яву']
    morning = ['доброго утра', 'хорошего утра']
    day = ['добрый день', 'хорошего дня']
    evening = ['добрый вечер', 'хорошего вечера']
    night = ['доброй ночи', 'хорошей ночи']
    goodbye = ['досвидания', 'всего вам хорошего', 'всего хорошего', 'пока', 'до скорого', 'прощайте']

    answer = ''
    if text in first_greeting or text in morning or text in day or text in evening or text in night:
        # получаем текущее время на компьтере
        t = time.localtime()
        # извлечем из полученных данны кокретное время (часы)
        curent_time = int(time.strftime('%H',t))
        if curent_time >= 0 and curent_time <=6:
             answer = night[random.randint(0, len(night)-1)]
        elif curent_time > 6 and curent_time <=12:
             answer = morning[random.randint(0, len(morning)-1)]
        elif curent_time > 12 and curent_time <=18:
             answer = day[random.randint(0, len(day)-1)]
        elif curent_time > 18 and curent_time <24:
             answer = evening[random.randint(0, len(evening)-1)]

    elif text in goodbye:
        answer = goodbye[random.randint(0, len(goodbye)-1)]

    # необходимо добавть elif  к внешенму if и проверить текст на прощание

    return answer != ""

# функция выдает погоду на день по городу Москва
def current_weather(appid, s_city = 'Moscow,RU', Ru_siti=''):
    city_id = 0
    # проверка на существование грода и его ID
    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/find',
                           params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        city_id = data['list'][0]['id']
    except Exception as e:

        return 'данный город не известен'

    # получение текущей температуры по городу

    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/weather',
               params = {'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        #print(res)
        result = "Погода по городу " + Ru_siti + ' температура :' + str(data['main']['temp']) \
               + ' максимальная температура :'+ str(data['main']['temp_max']) \
               + ' минммальная температура :' + str(data['main']['temp_min']) \
               + ' осодки :' + str(data['weather'][0]['description'])
    except Exception as e:
        print('Ошибка (поиска):', e)
    return result

    
# получение температуры по городу на 5 дней
def weather_on_5_day(appid, s_city = 'Moscow,RU', Ru_siti=''):
      # проверка на существование грода и его ID
    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/find',
                           params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        city_id = data['list'][0]['id']
    except Exception as e:
       return 'данный город не известен'

    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/forecast',
                           params={'id': city_id, 'units': 'metric', 'long': 'ru', 'APPID': appid})
        data = res.json()

        result = "Погода по городу " + Ru_siti + ' температура :'
        for i in data['list']:
            result += i['dt_txt'] + ' Температура: {0:+3.0f}'.format(i['main']['temp']) + ' ' + i['weather'][0]['description'] + "\n"
    
    except Exception as e:
        print('Ошибка (поиска):', e)
    return result

# погода на 5 дней краткая
def weather_on_5_day_briefly(appid, s_city='Moscow,RU', Ru_siti=''):
    # проверка на существование грода и его ID
    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/find',
                           params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        city_id = data['list'][0]['id']
    except Exception as e:
        return 'данный город не известен'

    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/forecast',
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        count = 0
        summ = 0
        result = "Погода по городу " + Ru_siti + ' температура :'
        count_1 = True
        for i in data['list']:
                tame = i['dt_txt'].split()

                if tame[1] == '00:00:00':
                    if count_1 == True:
                        tame_1 = tame[0]

                    summ = summ/count
                    result += tame_1 + ' Температура: {0:+3.0f}'.format(summ) + ' ' + i['weather'][0][
                'description'] + "\n"
                    count = 0
                    summ = 0
                summ += i['main']['temp']
                count += 1
                tame_1 = tame[0]
                count_1 = False

    except Exception as e:
        print('Ошибка (поиска):', e)
    return result


# погода на один день расширенная(каждые 3 часа)
def weather_on_1_day_extended(appid, s_city='Moscow,RU', Ru_siti=''):
    # проверка на существование грода и его ID
    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/find',
                           params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        city_id = data['list'][0]['id']
    except Exception as e:
        return 'данный город не известен'

    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/forecast',
                           params={'id': city_id, 'units': 'metric', 'long': 'ru', 'APPID': appid})
        data = res.json()

        result = "Погода по городу " + Ru_siti + ' температура :'
        for i in data['list']:
            tame = i['dt_txt'].split()[1]
            if tame == '00:00:00':
                break
            result += i['dt_txt'] + ' Температура: {0:+3.0f}'.format(i['main']['temp']) + ' ' + i['weather'][0][
                'description'] + "\n"

    except Exception as e:
        print('Ошибка (поиска):', e)
    return result


def weather(text):
    global answer
    answer = ''
    text = text.split()
    text[1]= text[1][0].upper()+text[1][1::]
    if text[0] != 'погода':
        return False
    # перевдем название города русского языка на наглийский
    # при вызове переовза можно указать следующие параметры:
    # src - исходный язык(если не указан конкретный язык система автомтичечки будет его распозновать)
    # dest - язык на кокой переводи(по умолчанию английский)
    # origin  - текст , который необходимо превести
    # создадим объект для переводчка
    trans = Translator()
    # произведем перевод
    print(text[1])
    name_syti = trans.translate(text[1])
    print(name_syti)
    # указать полученый API-ключ отсайта
    appid = 'ecf8f7c99b22ef5a327aa9d6f296cc4c'
    new_taxt = ' '.join(text[2::])
    if new_taxt == 'на один день':
        answer = current_weather(appid, name_syti.text + ',RU', text[1])
    elif new_taxt == 'на пять дней':
        answer = weather_on_5_day(appid, name_syti.text + ',RU', text[1])
    elif new_taxt == "на один день расширенная":
        answer = weather_on_1_day_extended(appid, name_syti.text + ',RU', text[1])
    elif new_taxt == 'на пять дней кратко':
        answer = weather_on_5_day_briefly(appid, name_syti.text + ',RU', text[1])
    current_date = datetime.now()
    current_date = str(current_date).split('.')[0]
    current_date = current_date.replace(':','_')
    # запишем данные в файл (параметр 'w' указывает на перезщапись файла, если паратмтер 'a' - дозапись файла(добавление новой записи в документ))
    with open('Погода\Погода ' + text[1]+ " "  + current_date +'.txt', 'w') as file:
        file.write(answer)
    return answer != ''

    # ф-ция обработки текста и выделения из них команд
def comands(text):

    if hi_goodby(text) or weather(text) or play_file(text) or goole_search(text):
        print(answer)
        sound(engin, answer)


    else:
        print(" я вас не поняла ")

# ф-ция нахожения файла по имени с возможностью указать расширение файла. На входе подставляем имя файла,
# при необходимости его расширение и диск на котором нужно искать файл

def file_search(my_path, name_file, expansion):
    # ф-ция walk находит все файлы по указанному пути
    for root_dir, dirs, files in os.walk(my_path):
        for file in files:
            # выражение разбивает название файла на имя файла и его расширение с помощью функци split
            file = file.lower()
            if file.split('.')[-1] == expansion:
                # ф-ция join  из модуля os.path объединят путь к папке и имя файла в полноценный путь
                name = os.path.join(root_dir, file)
                # производим поиск  искомого файла после фльтрации по расширению из оставшихся файлов одного расширения
                new_file = file.lower()
                if new_file.find(name_file)>-1:
                    list_file.append(name)

# ф-ция нахоженич всех файлов по запросу на ПК и отображения результатов пользовотилю
def play_file(text):
    # команда для поиска файлов: файл,вид документа,название документа
    list_data = text.split()
    if list_data[0] != 'файл':
        return False
    list_disk =list()
    disks = psutil.disk_partitions()
    global list_file
    for i in disks:
        list_disk.append(i[0])
    if list_data[1] == 'музыка':
        list_file = list()
        name_file = ' '.join(list_data[2:len(list_data)])
        for disk in list_disk:
            file_search(disk, name_file, 'mp3')
    elif list_data[1] == 'текст':
        list_file = list()
        name_file = ' '.join(list_data[2:len(list_data)])
        for disk in list_disk:
            file_search(disk, name_file, 'docx')

    #  дополнить разилчными поисковыми запросами. возможно добаваить неограниченное коилчество запросов на поиск данных
    global answer
    answer = ''
    if len(list_file)>0:
        for file in list_file:
            print(file)
        answer = 'файлы найдены'
        # запустим первый найденый файл в роднм приложении
        os.startfile(list_file[0])
        """
        # запустими все найденные файлы
        for i in range(len(list_file)):
            os.startfile(list_file[i])
        """
    else:
        answer = 'файлы не найдены'
    return True

def goole_search(name_search=''):
    print(name_search)
    name_search = name_search.split()
    print(name_search)
    if name_search[0] != 'онлайн':
        return False
    name_search = ' '.join(name_search[1:len(name_search)])
    print(name_search)
    name_search = name_search.replace(" ", "+")
    url = f"http://www.google.com/search?q={name_search}"
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intell Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent": USER_AGENT}
    page = requests.get(url, headers=headers)
    #print(page)
    result = BeautifulSoup(page.content, "html.parser")
    #print(result)
    result_url = []
    # print(result.find_all("div", class_="g"))
    for g in result.find_all("div", class_="g"):
        anchors = g.find_all("a")
        if anchors:
            link = anchors[0]["href"]
            title = g.find("h3").text
            item = {"title": title, "link": link}
            result_url.append(item)
    # откроем первую из найденных ссылок в браузере
    # print(len(result_url))
    print("полученные результаты запроса")
    for data_link in  result_url:
        print(data_link.get('title'))
        print(data_link.get('link'))
        print('_________')
    global answer
    answer = 'по вашему запросу найдены '+ str(len(result_url))+ 'ссылок'
    url = result_url[0].get('link')
    webbrowser.open(url)
    return True

# функция распозания речи
def recognize_speech():
    audio = 'я Вас не поняла'
    with microphon:
        data = ''
        # регулировка окружаюещго шума
        recognizer.adjust_for_ambient_noise(microphon, duration = 2)
        try:
            print("скажите команду: ")
            # получим данные с миукрофона ввиде аудиопересменной
            audio = recognizer.listen(microphon, 2,2)
        except Exception as ex:
            print('ошибка : ', ex)
            return ''
        # распознание аудио онлайн через гугл
        data = recognizer.recognize_google(audio, language= 'ru')
        return data.lower()

#weather('погода Билибино на пять дней кратко' )
#print(answer)
#goole_search('онлайн Дом')
#print(answer)
'''
engin = init_engine()
#sound(engin, "Привет , как у тебя дела, какая у тебя дома погода и сколько тебе лет")
#print(googletrans.LANGUAGES)
'''
while True:
    text = recognize_speech()
    comands(text)
'''    
'''


#play_file('файл текст виктор')
#print(list_file)
#file_search('C:\Python_version2\independent_work_2','2','py')
# print('вы сказади :', recognize_speech())
#init_engine()

