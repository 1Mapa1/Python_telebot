import json


import telebot
from telebot import types
import random
from os import path

token = '5575230601:AAEKgwuQqpmwgdzOGvImyT5aNlxI5RMYxKw'

bot = telebot.TeleBot(token)
hp = damage = exp = 0
lvl = 1
login = ""
password = ""
race_database = {
    'Эльф': {'hp': 15, 'damage': 35},
    'Гном': {'hp': 35, 'damage': 20},
    'Человек': {'hp': 25, 'damage': 25}
}
prof_database = {
    'Лучник': {'hp': 25, 'damage': 35},
    'Воин': {'hp': 50, 'damage': 20},
    'Маг': {'hp': 15, 'damage': 70}
}


def write_state():
    global login, hp, damage, exp, lvl
    with open("users.json", 'r') as file:
        dict = json.load(file)
    for user in dict["user"]:
        if user["name"] == login:
            hp = user['hp']
            damage = user['damage']
            lvl = user['lvl']
            exp = user['exp']


def chake_login(login):
    with open("users.json", 'r') as file:
        dict = json.load(file)
    for user in dict["user"]:
        if user["name"] == login:
            return True
    return False


def chake_password(password):
    global login
    with open("users.json", 'r') as file:
        dict = json.load(file)
    for user in dict["user"]:
        if user["name"] == login:
            if user["password"] == password:
                return True
    return False


def make_restart_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("С начала")
    markup.add(btn1)
    return markup


def make_race_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for race in race_database.keys():
        markup.add(types.KeyboardButton(text=race))
    return markup


def make_prof_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for prof in prof_database.keys():
        markup.add(types.KeyboardButton(text=prof))
    return markup


def create_monster():
    rnd_name = random.choice(monster)
    rnd_hp = random.randint(10, 10)
    rnd_damage = random.randint(13, 17)
    return [rnd_name, rnd_hp, rnd_damage]


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать игру")
    btn2 = types.KeyboardButton("Об игре...")
    btn3 = types.KeyboardButton("Выйти")
    markup.add(btn1, btn2, btn3)
    return markup


@bot.message_handler(commands=['start'])
def start_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Войти")
    btn2 = types.KeyboardButton("Зарегистрироваться")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text='Добро пожаловать в подземелье!', reply_markup=markup)


@bot.message_handler(commands=["save"])
def save(message):
    global login, hp, damage, exp, lvl
    with open("users.json", 'r') as file:
        dict = json.load(file)
    for user in dict["user"]:
        if user["name"] == login:
            user['hp'] = hp
            user['damage'] = damage
            user['lvl'] = lvl
            user['exp'] = exp

    with open("users.json", 'w') as file:
        json.dump(dict, file, indent=4)
    start_menu(message)


def start_quest():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = 'В путь!'
    btn2 = 'Вернуться в главное меню'
    markup.add(btn1, btn2)
    return markup


@bot.message_handler(content_types=['text'])
def main(message):
    global hp, damage, exp, lvl
    victim = create_monster()
    if (message.text == "Выйти"):
        save(message)
    if (message.text == "C начала"):
        start_menu(message)
    if (message.text == "Зарегистрироваться"):
        bot.send_message(message.chat.id, "Придумайте логин: ")
        bot.register_next_step_handler(message, get_login, False)
    if (message.text == "Войти"):
        bot.send_message(message.chat.id, "Введите логин: ")
        bot.register_next_step_handler(message, get_login, True)
    if (message.text == "Начать игру"):
        if hp != "0":
            bot.send_message(message.chat.id, text='Продолжаем путь? ', reply_markup=start_quest())
        else:
            bot.send_message(message.chat.id, text='Выбери расу персонажа:', reply_markup=make_race_menu())
    elif (message.text == "Вернуться в главное меню"):
        bot.send_message(message.chat.id, text='Вы вернулись в главное меню', reply_markup=main_menu())
    if (message.text == 'Эльф'):
        hp += race_database['Эльф']['hp']
        damage += race_database['Эльф']['damage']
        text = f'Вы высокородный эльф, и сейчас ваше здоровье равно:{hp}, а урон равен:{damage}. Осталось выбрать профессию'
        img = open('game/elf.jpg', 'rb')
        bot.send_photo(message.chat.id, img, caption=text, reply_markup=make_prof_menu())

        # bot.send_message(message.chat.id, reply_markup = make_prof_menu())
    if (message.text == 'Гном'):
        hp += race_database['Гном']['hp']
        damage += race_database['Гном']['damage']
        text = f'Вы крепкий гном, и сейчас ваше здоровье равно:{hp}, а урон равен:{damage}. Осталось выбрать профессию'
        img = open('game/gnom.jpg', 'rb')
        bot.send_photo(message.chat.id, img, caption=text, reply_markup=make_prof_menu())

    if (message.text == 'Человек'):
        hp += race_database['Человек']['hp']
        damage += race_database['Человек']['damage']
        text = f'Вы бесстрашный герой, и сейчас ваше здоровье равно:{hp}, а урон равен:{damage}. Осталось выбрать профессию'
        img = open('game/chel.jpg', 'rb')
        bot.send_photo(message.chat.id, img, caption=text, reply_markup=make_prof_menu())
    if (message.text == 'Лучник'):
        hp += prof_database['Лучник']['hp']
        damage += prof_database['Лучник']['damage']
        text = f'Вы высококлассный лучник, а это значит, что ваше здоровье равно:{hp}, а урон равен:{damage}. Вперед к приключениям?'
        img = open('game/lyk.png', 'rb')
        bot.send_photo(message.chat.id, img, caption=text, reply_markup=start_quest())
    if (message.text == 'Воин'):
        hp += prof_database['Воин']['hp']
        damage += prof_database['Воин']['damage']
        text = f'Вы неудержимый боец, а это значит, что ваше здоровье равно:{hp}, а урон равен:{damage}. Вперед к приключениям?'
        img = open('game/mech.jpg', 'rb')
        bot.send_photo(message.chat.id, img, caption=text, reply_markup=start_quest())
    if (message.text == 'Маг'):
        hp += prof_database['Маг']['hp']
        damage += prof_database['Маг']['damage']
        text = f'Вы могущественный маг, а это значит, что ваше здоровье равно:{hp}, а урон равен:{damage}. Вперед к приключениям?'
        img = open('game/posoh.jpg', 'rb')
        bot.send_photo(message.chat.id, img, caption=text, reply_markup=start_quest())

    if (message.text == 'В путь!'):
        event = random.randint(1, 4)
        if event == 2:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button3 = 'В путь!'
            button4 = 'Вернуться в главное меню'
            markup.add(button3, button4)
            bot.send_message(message.chat.id, text="Пока никто не встретился... Идём дальше?", reply_markup=markup)
        elif event == 1 or event == 3 or event == 4:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button5 = 'Атаковать'
            button6 = 'Бежать'
            button7 = 'Вернуться в главное меню'
            # victim = create_monster()
            print(type(victim))
            markup.add(button5, button6, button7)
            bot.send_message(message.chat.id,
                             text=f"Ого! Встретился монстр! Монстра зовут {victim[0]}, у него {victim[1]} очков здоровья и вот такой урон:{victim[2]} ",
                             reply_markup=markup)
    if (message.text == 'Атаковать'):
        victim[1] -= damage
        print(victim[1])
        if victim[1] <= 0:
            exp += 10 * lvl
            if exp >= lvl * 30:
                lvl += 1
                hp += 25 * lvl
                damage += 15 * lvl

                bot.send_message(message.chat.id, text=f'Твой уровень повысился! \
Теперь у тебя {lvl} уровень. hp:{hp}, damage:{damage}')
            bot.send_message(message.chat.id, text=f'Враг повержен! За победу\
ты получаешь {10 * lvl} очков опыта. Теперь у тебя: {exp} очков. Продожаем путешествие?', reply_markup=start_quest())
        elif victim[1] > 0:
            hp -= victim[2]
            print(hp)

            bot.send_message(message.chat.id, text=f'Монстр атакаует!')
            if hp <= 0:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1 = 'Вернуться в главное меню'
                markup.add(button1)
                bot.send_message(message.chat.id, text='Победа осталась за монстром!', reply_markup=markup)
            elif hp > 0:
                bot.send_message(message.chat.id, text=f' Теперь у монстра {victim[1]} \
очков здоровья и {victim[2]} урон, а у тебя {hp} очков здоровья. Что будешь делать?', reply_markup=combat())
    elif (message.text == 'Бежать'):
        plan = random.randint(1, 2)
        if plan == 1:
            bot.send_message(message.chat.id, text=f'Вы сумели сбежать от монстра! Продожаем путешествие?',
                             reply_markup=start_quest())
        elif plan == 2:
            hp -= victim[2]
            bot.send_message(message.chat.id, text=f'О ужас! Побег не удался и монстр атакаует!')
            if hp <= 0:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1 = 'Вернуться в главное меню'
                markup.add(button1)
                bot.send_message(message.chat.id, text='Победа осталась за монстром!', reply_markup=markup)
            elif hp > 0:
                bot.send_message(message.chat.id, text=f' Теперь у монстра {victim[1]} \
очков здоровья и {victim[2]} урон, а у тебя {hp} очков здоровья. Что будешь делать?', reply_markup=combat())


def get_login(message, log):
    global login
    if message.text == "С начала":
        start_menu(message)
    else:
        if log:
            if chake_login(message.text):
                bot.send_message(message.chat.id, "Введите пароль: ", reply_markup=make_restart_menu())
                login = message.text
                bot.register_next_step_handler(message, login_user)
            else:
                bot.send_message(message.chat.id, "Неправильный логин. Попробуйте снова ",
                                 reply_markup=make_restart_menu())
                bot.register_next_step_handler(message, get_login, True)
        else:
            login = message.text
            bot.send_message(message.chat.id, "Придумайте пароль: ", reply_markup=make_restart_menu())
            bot.register_next_step_handler(message, save_user)


def login_user(message):
    global password, login, hp, exp, damage, lvl
    if message.text == "С начала":
        start_menu(message)
    else:
        if chake_password(message.text):
            write_state()
            bot.send_message(message.chat.id,
                             text=f'Привет {login}. \nТвои характеристики: урон = {damage}, здоровье = {hp}, уровень = {lvl}, опыт = {exp}. \nГотов поиграть?',
                             reply_markup=main_menu())
        else:
            bot.send_message(message.chat.id, "Неправильный пароль: ", reply_markup=make_restart_menu())
            bot.register_next_step_handler(message, login_user)


def save_user(message):
    global password, login
    password = message.text
    if not path.exists("users.json"):
        with open("users.json", 'w') as file:
            dict = {"user": []}
            dict["user"].append({
                "name": "Admin",
                "password": "123",
                "hp": "100",
                "damage": "100",
                "lvl": "1",
                "exp": '0'
            })
            json.dump(dict, file, indent=4)
    with open("users.json", 'r') as file:
        dict = json.load(file)
    dict["user"].append({
        "name": login,
        "password": password,
        "hp": "0",
        "damage": "0",
        "lvl": "1",
        "exp": '0'
    })
    with open("users.json", 'w') as file:
        json.dump(dict, file, indent=4)
    bot.send_message(message.chat.id, text=f'Привет {login}, готов поиграть?', reply_markup=main_menu())


monster = ['Вася', 'Петя', 'Маша', 'Даша']
bot.polling(non_stop=True)




