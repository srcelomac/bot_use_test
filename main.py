import webbrowser
import telebot
import random
import requests
import json
from telebot import *
import string
import sqlite3
import math

bot = telebot.TeleBot('7196357802:AAHsMTbnuQiDM4ahfAtZihk8gU83mxPP58M')

yandex_cloud_catalog = "b1g4ptm2o8gu4v21foc5"
yandex_api_key = "AQVN38b3z0pR8frNt3gK0HZ6ynGLVQ0L1p_1gajc"
yandex_gpt_model = "yandexgpt"
system_prompt = "Придумай очень короткую ассоциацию, которую легко запомнить, например: дефИс - денИс. Ассоциацию ты должен придумать для того, чтобы ученик запомнил ударение в присланном тебе слове (правильное ударение указано заглавное буквой). В ответ напиши только самое предложение с ассоцацией, также тебе нельзя использовать никакой форматирование, ударение выделяй заглавной буквой."


'''
yandex_cloud_catalog = "b1g4ptm2o8gu4v21foc5"
yandex_gpt_api_key = "AQVN38b3z0pR8frNt3gK0HZ6ynGLVQ0L1p_1gajc"
yandex_gpt_model = "yandexgpt-lite"
'''

conn = sqlite3.connect('tasks.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Tasks (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, user_id INTEGER, task_id INTEGER, words TEXT, answers TEXT)')
conn.commit()
cur.close()
conn.close()

conn = sqlite3.connect('stats.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Stats (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, user_id INTEGER UNIQUE, rights INTEGER DEFAULT 0, wrongs INTEGER DEFAULT 0)')
conn.commit()
cur.close()
conn.close()


task_id = 0

task_4 = [
    ['аэропорты', 'аэропОрты'],
    ['банты', 'бАнты'],
    ['бороду', 'бОроду'],
    ['бухгалтеров', 'бухгАлтеров'],
    ['вероисповедание', 'вероисповЕдание'],
    ['водопровод', 'водопровОд'],
    ['газопровод', 'газопровОд'],
    ['гражданство', 'граждАнство'],
    ['дефис', 'дефИс'],
    ['дешевизна', 'дешевИзна'],
    ['диспансер', 'диспансЕр'],
    ['договорённость', 'договорЁнность'],
    ['документ', 'докумЕнт'],
    ['досуг', 'досУг'],
    ['еретик', 'еретИк'],
    ['жалюзи', 'жалюзИ'],
    ['значимость', 'знАчимость'],
    ['иксы', 'Иксы'],
    ['каталог', 'каталОг'],
    ['квартал', 'квартАл'],
    ['километр', 'киломЕтр'],
    ['конусов', 'кОнусов'],
    ['корысть', 'корЫсть'],
    ['краны', 'крАны'],
    ['кремень, кремня', 'кремЕнь, кремнЯ'],
    ['лекторов', 'лЕкторов'],
    ['локтя, локтей', 'лОктя, локтЕй'],
    ['лыжня', 'лыжнЯ'],
    ['местностей', 'мЕстность'],
    ['намерение', 'намЕрение'],
    ['нарост', 'нарОст'],
    ['недруг', 'нЕдруг'],
    ['недуг', 'недУг'],
    ['некролог', 'некролОг'],
    ['ненависть', 'нЕнависть'],
    ['нефтепровод', 'нефтепровОд'],
    ['новостей', 'новостЕй'],
    ['ногтя, ногтей', 'нОгтя, ногтЕй'],
    ['отзыв (о книге)', 'Отзыв'],
    ['отзыв (посла из страны)', 'отзЫв'],
    ['отрочество', 'Отрочество'],
    ['партнер', 'партЕр'],
    ['портфель', 'портфЕль'],
    ['поручни', 'пОручни'],
    ['приданое', 'придАное'],
    ['призыв', 'призЫв'],
    ['свёкла', 'свЁкла'],
    ['сироты', 'сирОты'],
    ['созыв', 'созЫв'],
    ['сосредоточение', 'сосредотОчение'],
    ['средства', 'срЕдства'],
    ['статуя', 'стАтуя'],
    ['столяр', 'столЯр'],
    ['таможня', 'тамОжня'],
    ['торты', 'тОрт'],
    ['туфля', 'тУфля'],
    ['цемент', 'цемЕнт'],
    ['центнер', 'цЕнтнер'],
    ['цепочка', 'цепОчка'],
    ['шарфы', 'шАрфы'],
    ['шофер', 'шофЁр'],
    ['эксперт', 'экспЕрт'],
    ['верна, верный', 'вернА, вЕрный'],
    ['значимый', 'знАчимый'],
    ['красивее', 'КрасИвее'],
    ['кухонный', 'кУхонный'],
    ['ловка, ловкий', 'ловкА, лОвкий'],
    ['мозаичный', 'мозаИчный'],
    ['оптовый', 'оптОвый'],
    ['прозорливый', 'прозорлИвый'],
    ['сливовый', 'слИвовый'],
    ['брала, брать', 'бралА, брАть'],
    ['бралась, браться', 'бралАсь, брАться'],
    ['взяла', 'взялА'],
    ['взялась, взяться', 'взялАсь, взЯться'],
    ['влилась, влиться', 'влилАсь, влИться'],
    ['ворвалась, ворваться', 'ворвалАсь, ворвАться'],
    ['воспринять', 'воспринЯть'],
    ['воссоздала', 'воссоздалА'],
    ['вручит', 'вручИт'],
    ['гнала', 'гналА'],
    ['гналась', 'гналАсь'],
    ['добрала', 'добралА'],
    ['добралась', 'добралАсь'],
    ['дождалась', 'дождалАсь'],
    ['дозвонится', 'дозвонИтся'],
    ['дозировать', 'дозИровать'],
    ['ждала', 'ждалА'],
    ['жилось', 'жилОсь'],
    ['закупорить', 'закУпорить'],
    ['занять, занял, заняла, заняли', 'занЯть, зАнял, занялА, зАняли'],
    ['заперла', 'заперлА'],
    ['запломбировать', 'запломбировАть'],
    ['защемит', 'защемИт'],
    ['звала', 'звалА'],
    ['звонит', 'звонИт'],
    ['кашлянуть', 'кАшлянуть'],
    ['клала', 'клАла'],
    ['клеить', 'клЕить'],
    ['кралась', 'крАлась'],
    ['кровоточить', 'кровоточИть'],
    ['лгала', 'лгалА'],
    ['лила', 'лИлА'],
    ['лилась', 'лИлась'],
    ['наврала', 'навралА'],
    ['наделит', 'наделИт'],
    ['надорвалась', 'надорвалАсь'],
    ['назвалась', 'назвалАсь'],
    ['накренится', 'накренИтся'],
    ['налила', 'налилА'],
    ['нарвала', 'нарвалА'],
    ['начать, начал, начала, начали', 'начАть, нАчал, началА, нАчали'],
    ['обзвонит', 'обзвонИт'],
    ['облегчить, облегчит', 'облегчИть, облегчИт'],
    ['облилась', 'облилАсь'],
    ['обнялась', 'обнялАсь'],
    ['обогнала', 'обогналА'],
    ['ободрала', 'ободралА'],
    ['ободрить, ободрит', 'ободрИть, ободрИт'],
    ['ободриться, ободрится', 'ободрИться, ободрИтся'],
    ['обострить', 'обострИть'],
    ['одолжить, одолжит', 'одолжИть, одолжИт'],
    ['озлобить', 'озлОбить'],
    ['оклеить', 'оклЕить'],
    ['окружит', 'окружИт'],
    ['опошлить', 'опОшлить'],
    ['Осведомиться, осведомится', 'освЕдомиться, освЕдомится'],
    ['отбыла', 'отбылА'],
    ['отдала', 'отдалА'],
    ['откупорить', 'откУпорить'],
    ['отозвала', 'отозвалА'],
    ['отозвалась', 'отозвалАсь'],
    ['перезвонит', 'перезвонИт'],
    ['перелила', 'перелилА'],
    ['плодоносить', 'плодоносИть'],
    ['пломбировать', 'пломбировАть'],
    ['повторит', 'повторИт'],
    ['позвала', 'позвалА'],
    ['позвонит', 'позвонИт'],
    ['полила', 'полилА'],
    ['положить, положил', 'положИть, положИл'],
    ['понять, поняла', 'понЯть, понялА'],
    ['послала', 'послАла'],
    ['прибыть, прибыл, прибыла, прибыли', 'прибЫть, прИбыл, прибылА, прИбыли'],
    ['принять, принял, приняла, приняли', 'принЯть, прИнял, принялА, прИняли'],
    ['рвала', 'рвалА'],
    ['сверлит', 'сверлИт'],
    ['сняла', 'снялА'],
    ['соврала', 'совралА'],
    ['создала', 'создалА'],
    ['сорвала', 'сорвалА'],
    ['сорит', 'сорИт'],
    ['убрала', 'убралА'],
    ['углубить', 'углубИть'],
    ['укрепит', 'укрепИт'],
    ['черпать', 'чЕрпать'],
    ['щемит', 'щемИт'],
    ['щёлкать', 'щЁлкать'],
    ['довезённый', 'довезЁнный'],
    ['загнутый', 'зАгнутый'],
    ['занятый, занята', 'зАнятый, занятА'],
    ['запертый', 'зАпертый'],
    ['заселённый, заселена', 'заселЁнный, заселенА'],
    ['кормящий', 'кормЯщий'],
    ['кровоточащий', 'кровоточАщий'],
    ['наживший', 'нажИвший'],
    ['наливший', 'налИвший'],
    ['нанявшийся', 'нанЯвшийся'],
    ['начавший', 'начАвший'],
    ['начатый', 'нАчатый'],
    ['низведённый', 'низведЁнный'],
    ['облегчённый', 'облегчЁнный'],
    ['ободрённый', 'ободрЁнный'],
    ['обострённый', 'обострЁнный'],
    ['отключённый', 'отключЁнный'],
    ['повторённый', 'повторЁнный'],
    ['поделённый', 'поделЁнный'],
    ['понявший', 'понЯвший'],
    ['принятый, принята', 'прИнятый, принятА'],
    ['приручённый', 'приручЁнный'],
    ['проживший', 'прожИвший'],
    ['снята', 'снятА'],
    ['согнутый', 'сОгнутый'],
    ['углублённый', 'углублЁнный'],
    ['закупорив', 'закУпорив'],
    ['начав', 'начАв'],
    ['начавшись', 'начАвшись'],
    ['отдав', 'отдАв'],
    ['подняв', 'поднЯв'],
    ['поняв', 'понЯв'],
    ['прибыв', 'прибЫв'],
    ['создав', 'создАв'],
    ['вовремя', 'вОвремя'],
    ['доверху', 'дОверху'],
    ['донельзя', 'донЕльзя'],
    ['донизу', 'дОнизу'],
    ['досуха', 'дОсуха'],
    ['засветло', 'зАсветло'],
    ['затемно', 'зАтемно'],
    ['красивее', 'красИвее'],
    ['надолго', 'надОлго'],
    ['ненадолго', 'ненадОлго']
]


def diff_letters(a,b):
    return sum (a[i] != b[i] for i in range(min(len(a), len(b))))

def req_gptshka(mes):
    global system_prompt
    global yandex_cloud_catalog
    global yandex_gpt_model
    global yandex_api_key
    prompt = mes
    body = {
        "modelUri": f"gpt://{yandex_cloud_catalog}/{yandex_gpt_model}",
        "completionOptions": {"stream": False, "temperature": 0.6, "maxTokens": "2000"},
        "messages": [
            {"role": "system", "text": system_prompt},
            {"role": "user", "text": prompt},
        ],
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {yandex_api_key}",
        "x-folder-id": yandex_cloud_catalog,
    }

    response = requests.post(url, headers=headers, json=body)
    response_json = json.loads(response.text)
    print(response_json)
    operation_id = response_json["id"]
    url = f"https://llm.api.cloud.yandex.net/operations/{operation_id}"
    headers = {"Authorization": f"Api-Key {yandex_api_key}"}

    while True:
        response = requests.get(url, headers=headers)
        response_json = json.loads(response.text)
        done = response_json["done"]
        if done:
            break
        else:
            time.sleep(0.1)

    answer = response_json["response"]["alternatives"][0]["message"]["text"]
    return answer

def subject_selection(subject: str):
    body = {
        "modelUri": f"gpt://{yandex_cloud_catalog}/{yandexgpt-lite}",
        "completionOptions": {"stream": False, "temperature": 0.1, "maxTokens": "2000"},
        "messages": [
            {"role": "system", "text": system_prompt},
            {"role": "user", "text": subject},
        ],
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {yandex_gpt_api_key}",
        "x-folder-id": yandex_cloud_catalog,
    }

    response = requests.post(url, headers=headers, json=body)
    response_json = json.loads(response.text)
    operation_id = response_json["id"]

    url = f"https://llm.api.cloud.yandex.net/operations/{operation_id}"
    headers = {"Authorization": f"Api-Key {yandex_gpt_api_key}"}

    done = False
    while not done:
        response = requests.get(url, headers=headers)
        response_json = json.loads(response.text)
        done = response_json["done"]
        time.sleep(0.1)

    if response.status_code != 200:
        return "ERROR"

    answer = response_json["response"]["alternatives"][0]["message"]["text"]

    return answer


@bot.message_handler(commands=['start'])
def main(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Тренировка')
    btn2 = types.KeyboardButton('Моя статистика')
    btn3 = types.KeyboardButton('Добавить слово')
    markup.row(btn1, btn2, btn3)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

@bot.message_handler(commands=['admin'])
def main(message):
    #webbrowser.open('https://t.me/srcelomac')
    bot.send_message(message.chat.id, f'Держи, @srcelomac')


@bot.message_handler()
def main_menu(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Тренировка')
    btn2 = types.KeyboardButton('Моя статистика')
    btn3 = types.KeyboardButton('Добавить слово')
    markup.row(btn1, btn2, btn3)
    bot.send_message(message.chat.id, f'Что-то ещё?', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

step = 0
answer_true = 0
answer_false = 0

#print((len(task_4)))
@bot.message_handler()
def training_4(message):
    global step
    global answer_true
    global answer_false
    global yandex_gpt_model
    global yandex_gpt_api_key
    global yandex_cloud_catalog
    #print(step)
    if (step == 0):
        if (message.text.lower() == "стоп" or message.text == "Стоп"):
            #main_menu(message)
            #print("Выход")
            #bot.register_next_step_handler(message, main_menu)
            step = 0
            markup = types.ReplyKeyboardMarkup()
            btn1 = types.KeyboardButton('Тренировка')
            btn2 = types.KeyboardButton('Моя статистика')
            btn3 = types.KeyboardButton('Добавить слово')
            markup.row(btn1, btn2, btn3)
            bot.send_message(message.chat.id, f'Ты сделал верно {answer_true} из {answer_true+answer_false} заданий. Что-то ещё?', reply_markup=markup)
            answer_true = 0
            answer_false = 0
            bot.register_next_step_handler(message, on_click)
        else:
            #print(step)
            random.shuffle(task_4)
            markup = types.ReplyKeyboardMarkup()
            btn_stop = types.KeyboardButton('Стоп')
            markup.row(btn_stop)
            bot.send_message(message.chat.id, task_4[step][0], reply_markup=markup)
            step += 1
            bot.register_next_step_handler(message, training_4)
    elif (step > 0):
        if ((message.text).lower() == "стоп" or message.text == "Стоп"):
            #main_menu(message)
            #print("Выход")
            #bot.register_next_step_handler(message, main_menu)
            step = 0
            markup = types.ReplyKeyboardMarkup()
            btn1 = types.KeyboardButton('Тренировка')
            btn2 = types.KeyboardButton('Моя статистика')
            btn3 = types.KeyboardButton('Добавить слово')
            markup.row(btn1, btn2, btn3)
            bot.send_message(message.chat.id, f'Ты сделал верно {answer_true} из {answer_true+answer_false} заданий. Что-то ещё?', reply_markup=markup)
            answer_true = 0
            answer_false = 0
            bot.register_next_step_handler(message, on_click)
        elif (message.text[1::] == task_4[step-1][1][1::]):
            bot.send_message(message.chat.id, "Верно!")
            answer_true += 1
            conn = sqlite3.connect('stats.db')
            cur = conn.cursor()
            sqlite_select_query = f"""UPDATE Stats SET rights = rigths + 1 where user_id = {message.chat.id}"""
            cur.execute(sqlite_select_query)
            cur.close()
            conn.close()
            if (step >= len(task_4)):
                step = 0
                markup = types.ReplyKeyboardMarkup()
                btn1 = types.KeyboardButton('Тренировка')
                btn2 = types.KeyboardButton('Моя статистика')
                btn3 = types.KeyboardButton('Добавить слово')
                markup.row(btn1, btn2, btn3)
                bot.send_message(message.chat.id,
                                 f'Слова закончились. Ты молодец!\n Ты сделал верно {answer_true} из {answer_true + answer_false} заданий.',
                                 reply_markup=markup)
                answer_true = 0
                answer_false = 0
                bot.register_next_step_handler(message, on_click)
            else:
                bot.send_message(message.chat.id, task_4[step][0])
                step += 1
                #print('yep')
                bot.register_next_step_handler(message, training_4)
        else:
            #answer = req_gptshka(task_4[step-1][1])
            #answer = subject_selection(message.text)
            #bot.send_message(message.chat.id, f'Неверно! \nПравильный ответ: {task_4[step-1][1]} \nПопробуй запомнить так: {answer}')
            bot.send_message(message.chat.id,
                             f'Неверно! \nПравильный ответ: {task_4[step - 1][1]}')
            answer_false += 1
            conn = sqlite3.connect('stats.db')
            cur = conn.cursor()
            sqlite_select_query = f"""UPDATE Stats SET wrongs = wrongs + 1 where user_id = {message.chat.id}"""
            cur.execute(sqlite_select_query)
            cur.close()
            conn.close()
            if (step >= len(task_4)):
                step = 0
                markup = types.ReplyKeyboardMarkup()
                btn1 = types.KeyboardButton('Тренировка')
                btn2 = types.KeyboardButton('Моя статистика')
                btn3 = types.KeyboardButton('Добавить слово')
                markup.row(btn1, btn2, btn3)
                bot.send_message(message.chat.id,
                                 f'Слова закончились. Ты молодец!\nТы сделал верно {answer_true} из {answer_true + answer_false} заданий.',
                                 reply_markup=markup)
                answer_true = 0
                answer_false = 0
                bot.register_next_step_handler(message, on_click)
            else:
                bot.send_message(message.chat.id, task_4[step][0])
                step += 1
                #print("no")
                bot.register_next_step_handler(message, training_4)

task_words = []

@bot.message_handler()
def training(message):
    global task_id
    global step
    global answer_true
    global answer_false
    global task_words
    if (step == 0):
        if (message.text.lower() == "стоп" or message.text == "Стоп"):
            # main_menu(message)
            # print("Выход")
            # bot.register_next_step_handler(message, main_menu)
            step = 0
            task_id = 0
            task_words = []
            markup = types.ReplyKeyboardMarkup()
            btn1 = types.KeyboardButton('Тренировка')
            btn2 = types.KeyboardButton('Моя статистика')
            btn3 = types.KeyboardButton('Добавить слово')
            markup.row(btn1, btn2, btn3)
            bot.send_message(message.chat.id,
                             f'Ты сделал верно {answer_true} из {answer_true + answer_false} заданий. Что-то ещё?',
                             reply_markup=markup)
            answer_true = 0
            answer_false = 0
            bot.register_next_step_handler(message, on_click)
        else:
            conn = sqlite3.connect('tasks.db')
            cur = conn.cursor()
            sqlite_select_query = f"""SELECT words from Tasks where (user_id = {message.chat.id} and task_id = {task_id})"""
            cur.execute(sqlite_select_query)
            # cur.execute(f"SELECT words * FROM Tasks * WHERE user_id = {message.chat.id}")
            list_of_words = cur.fetchall()
            sqlite_select_query = f"""SELECT answers from Tasks where (user_id = {message.chat.id} and task_id = {task_id})"""
            cur.execute(sqlite_select_query)
            list_of_answers = cur.fetchall()
            cur.close()
            conn.close()
            for i in range(len(list_of_words)):
                s1 = str(list_of_words[i])
                s1 = s1.replace('(', '')
                s1 = s1.replace(')', '')
                s1 = s1.replace("'", '')
                s1 = s1.replace(',', '')
                s2 = str(list_of_answers[i])
                s2 = s2.replace('(', '')
                s2 = s2.replace(')', '')
                s2 = s2.replace("'", '')
                s2 = s2.replace(',', '')
                task_words.append([s1, s2])
                print(s1)
                print(s2)
            print(task_words)
            random.shuffle(task_words)
            markup = types.ReplyKeyboardMarkup()
            btn_stop = types.KeyboardButton('Стоп')
            markup.row(btn_stop)
            bot.send_message(message.chat.id, task_words[step][0], reply_markup=markup)
            step += 1
            bot.register_next_step_handler(message, training)
    elif (step > 0):
        if ((message.text).lower() == "стоп" or message.text == "Стоп"):
            # main_menu(message)
            # print("Выход")
            # bot.register_next_step_handler(message, main_menu)
            step = 0
            task_id = 0
            task_words = []
            markup = types.ReplyKeyboardMarkup()
            btn1 = types.KeyboardButton('Тренировка')
            btn2 = types.KeyboardButton('Моя статистика')
            btn3 = types.KeyboardButton('Добавить слово')
            markup.row(btn1, btn2, btn3)
            bot.send_message(message.chat.id,
                             f'Ты сделал верно {answer_true} из {answer_true + answer_false} заданий. Что-то ещё?',
                             reply_markup=markup)
            answer_true = 0
            answer_false = 0
            bot.register_next_step_handler(message, on_click)
        elif (message.text[1::] == task_words[step - 1][1][1::]):
            bot.send_message(message.chat.id, "Верно!")
            answer_true += 1
            conn = sqlite3.connect('stats.db')
            cur = conn.cursor()
            sqlite_select_query = f"""UPDATE Stats SET rights = rights + 1 where user_id = {message.chat.id}"""
            cur.execute(sqlite_select_query)
            cur.close()
            conn.close()
            if (step >= len(task_words)):
                step = 0
                markup = types.ReplyKeyboardMarkup()
                btn1 = types.KeyboardButton('Тренировка')
                btn2 = types.KeyboardButton('Моя статистика')
                btn3 = types.KeyboardButton('Добавить слово')
                markup.row(btn1, btn2, btn3)
                bot.send_message(message.chat.id,
                                 f'Слова закончились. Ты молодец!\n Ты сделал верно {answer_true} из {answer_true + answer_false} заданий.',
                                 reply_markup=markup)
                answer_true = 0
                answer_false = 0
                bot.register_next_step_handler(message, on_click)
            else:
                bot.send_message(message.chat.id, task_words[step][0])
                step += 1
                # print('yep')
                bot.register_next_step_handler(message, training)
        else:
            # answer = req_gptshka(task_4[step-1][1])
            # answer = subject_selection(message.text)
            # bot.send_message(message.chat.id, f'Неверно! \nПравильный ответ: {task_4[step-1][1]} \nПопробуй запомнить так: {answer}')
            bot.send_message(message.chat.id,
                             f'Неверно! \nПравильный ответ: {task_words[step - 1][1]}')
            answer_false += 1
            conn = sqlite3.connect('stats.db')
            cur = conn.cursor()
            sqlite_select_query = f"""UPDATE Stats SET wrongs = wrongs + 1 where user_id = {message.chat.id}"""
            cur.execute(sqlite_select_query)
            cur.close()
            conn.close()
            if (step >= len(task_words)):
                step = 0
                markup = types.ReplyKeyboardMarkup()
                btn1 = types.KeyboardButton('Тренировка')
                btn2 = types.KeyboardButton('Моя статистика')
                btn3 = types.KeyboardButton('Добавить слово')
                markup.row(btn1, btn2, btn3)
                bot.send_message(message.chat.id,
                                 f'Слова закончились. Ты молодец!\nТы сделал верно {answer_true} из {answer_true + answer_false} заданий.',
                                 reply_markup=markup)
                answer_true = 0
                answer_false = 0
                bot.register_next_step_handler(message, on_click)
            else:
                bot.send_message(message.chat.id, task_words[step][0])
                step += 1
                # print("no")
                bot.register_next_step_handler(message, training)


flag_add = False
word_was = False
@bot.message_handler()
def add_task(message):
    global flag_add
    global task_id
    global word_was
    if (flag_add == False):
        markup = types.ReplyKeyboardMarkup()
        btn_stop = types.KeyboardButton('Стоп')
        markup.row(btn_stop)
        bot.send_message(message.chat.id, "На первой строке напиши слово с пропуском '_', на второй правильный ответ", reply_markup=markup)
        flag_add = True
        bot.register_next_step_handler(message, add_task)
    else:
        print(message.text.split('\n'))
        new_pair = [x.lower() for x in message.text.strip().split('\n')]
        if ((message.text).lower() == "стоп" or message.text == "Стоп"):
            # main_menu(message)
            # print("Выход")
            # bot.register_next_step_handler(message, main_menu)
            flag_add = 0
            task_id = 0
            markup = types.ReplyKeyboardMarkup()
            btn1 = types.KeyboardButton('Тренировка')
            btn2 = types.KeyboardButton('Моя статистика')
            btn3 = types.KeyboardButton('Добавить слово')
            markup.row(btn1, btn2, btn3)
            bot.send_message(message.chat.id, "Хорошо!", reply_markup=markup)
            bot.register_next_step_handler(message, on_click)
        elif (len(message.text.strip().split('\n')) == 2) and (diff_letters(new_pair[0], new_pair[1]) == 1):
            conn = sqlite3.connect('tasks.db')
            cur = conn.cursor()
            sqlite_select_query = f"""SELECT * from Tasks where user_id = {message.chat.id}"""
            cur.execute(sqlite_select_query)
            #cur.execute(f"SELECT words * FROM Tasks * WHERE user_id = {message.chat.id}")
            list_of_words = cur.fetchall()
            cur.close()
            conn.close()
            word_was = False
            for _ in list_of_words:
                print(_)
                if (new_pair[0] in _):
                    word_was = True
                    break
            if (not(word_was)):
                conn = sqlite3.connect('tasks.db')
                cur = conn.cursor()
                cur.execute('INSERT INTO Tasks (user_id, task_id, words, answers) VALUES (?, ?, ?, ?)',
                            (message.chat.id, task_id, new_pair[0], new_pair[1]))
                conn.commit()
                cur.close()
                conn.close()
                bot.send_message(message.chat.id, "Добавлено!")
                bot.register_next_step_handler(message, add_task)
            else:
                bot.send_message(message.chat.id, "Это слово уже добавлено")
                word_was = False
                bot.register_next_step_handler(message, add_task)
        else:
            bot.send_message(message.chat.id, "Где-то ошибка, проверьте корректность")
            bot.register_next_step_handler(message, add_task)


@bot.message_handler()
def on_click(message):
    #print(message.text)
    if message.text == 'Тренировка':
        markup = types.ReplyKeyboardMarkup()
        btn_task4 = types.KeyboardButton('4')
        btn_task9 = types.KeyboardButton('9')
        btn_task10 = types.KeyboardButton('10')
        btn_task11 = types.KeyboardButton('11')
        btn_task12 = types.KeyboardButton('12')
        btn_task13 = types.KeyboardButton('13')
        btn_task14 = types.KeyboardButton('14')
        btn_task15 = types.KeyboardButton('15')
        markup.row(btn_task4, btn_task9, btn_task10, btn_task11, btn_task12, btn_task13, btn_task14, btn_task15)
        bot.send_message(message.chat.id, f'Каким заданием хочешь заняться?', reply_markup=markup)
        bot.register_next_step_handler(message, on_click_task)
    elif message.text == 'Моя статистика':
        conn = sqlite3.connect('stats.db')
        cur = conn.cursor()
        sqlite_select_query = f"""SELECT rights from Stats where user_id = {message.chat.id}"""
        cur.execute(sqlite_select_query)
        right = cur.fetchall()
        sqlite_select_query = f"""SELECT wrongs from Stats where user_id = {message.chat.id}"""
        cur.execute(sqlite_select_query)
        wrong = cur.fetchall()
        print(right)
        print(wrong)
        cur.close()
        conn.close()
        bot.send_message(message.chat.id,
                         f'Ты сделал верно {right} из {right + wrong} заданий ({math.ceil(right/(right+wrong)*100)}%). Что-то ещё?')
    elif message.text == 'Добавить слово':
        markup = types.ReplyKeyboardMarkup()
        btn_task9 = types.KeyboardButton('9')
        btn_task10 = types.KeyboardButton('10')
        btn_task11 = types.KeyboardButton('11')
        btn_task12 = types.KeyboardButton('12')
        btn_task13 = types.KeyboardButton('13')
        btn_task14 = types.KeyboardButton('14')
        btn_task15 = types.KeyboardButton('15')
        markup.row(btn_task9, btn_task10, btn_task11, btn_task12, btn_task13, btn_task14, btn_task15)
        bot.send_message(message.chat.id, f'В какое задание хочешь добавить слово?', reply_markup=markup)
        bot.register_next_step_handler(message, on_click_task_add)

def on_click_task(message):
    global task_id
    if (message.text == '4'):
        #print('*')
        training_4(message)
    else:
        task_id = int(message.text)
        training(message)


def on_click_task_add(message):
    global task_id
    task_id = int(message.text)
    add_task(message)



bot.polling(none_stop=True)
