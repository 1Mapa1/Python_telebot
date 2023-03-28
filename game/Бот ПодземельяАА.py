import telebot
from telebot import types
import random


token = '5575230601:AAEKgwuQqpmwgdzOGvImyT5aNlxI5RMYxKw'

bot = telebot.TeleBot(token)
hp = damage = exp = 0
lvl = 1
race_database = {
    'Эльф': {'hp': 15, 'damage': 35},
    'Гном' : {'hp': 35, 'damage' : 20},
    'Человек' : {'hp': 25, 'damage': 25}
    }
prof_database = {
    'Лучник': {'hp': 25, 'damage' : 35},
    'Воин': {'hp': 50, 'damage': 20},
    'Маг' : {'hp': 15, 'damage': 70}
}

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
    rnd_hp = random.randint(130,155)
    rnd_damage = random.randint(130, 170)
    return [rnd_name, rnd_hp, rnd_damage]

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать игру")
    btn2 = types.KeyboardButton("Об игре...")
    markup.add(btn1, btn2)
    return markup

@bot.message_handler(commands=['start'])
def start_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать игру")
    btn2 = types.KeyboardButton("Об игре...")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text = 'Привет, готов поиграть?', reply_markup = markup)

def start_quest():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = 'В путь!'
    btn2 = 'Вернуться в главное меню'
    markup.add(btn1, btn2)
    return markup

@bot.message_handler(content_types=['text'])
def main(message):
    global hp, damage
    victim = create_monster()
    if (message.text == "Начать игру"):
        bot.send_message(message.chat.id, text='Выбери расу персонажа:', reply_markup=make_race_menu())
    elif (message.text == "Вернуться в главное меню"):
        hp = damage = 0
        bot.send_message(message.chat.id, text = 'Вы вернулись в главное меню', reply_markup = main_menu())
    if (message.text == 'Эльф'):
        hp += race_database['Эльф']['hp']
        damage += race_database['Эльф']['damage']
        text = f'Вы высокородный эльф, и сейчас ваше здоровье равно:{hp}, а урон равен:{damage}. Осталось выбрать профессию'
        img = open('elf.jpg', 'rb')
        bot.send_photo(message.chat.id, img, caption = text, reply_markup = make_prof_menu())
        
        #bot.send_message(message.chat.id, reply_markup = make_prof_menu())
    if (message.text == 'Гном'):
        hp += race_database['Гном']['hp']
        damage += race_database['Гном']['damage']
        text =f'Вы крепкий гном, и сейчас ваше здоровье равно:{hp}, а урон равен:{damage}. Осталось выбрать профессию'
        img = open('gnom.jpg', 'rb')
        bot.send_photo(message.chat.id, img, caption = text, reply_markup = make_prof_menu())
        
    if (message.text == 'Человек'):
        hp += race_database['Человек']['hp']
        damage += race_database['Человек']['damage']
        text = f'Вы бесстрашный герой, и сейчас ваше здоровье равно:{hp}, а урон равен:{damage}. Осталось выбрать профессию'
        img = open('chel.jpg', 'rb')
        bot.send_photo(message.chat.id, img, caption = text, reply_markup = make_prof_menu())        
    if (message.text == 'Лучник'):
        hp += prof_database['Лучник']['hp']
        damage+= prof_database['Лучник']['damage']
        text = f'Вы высококлассный лучник, а это значит, что ваше здоровье равно:{hp}, а урон равен:{damage}. Вперед к приключениям?'
        img = open('lyk.png', 'rb')
        bot.send_photo(message.chat.id, img, caption = text, reply_markup = start_quest()) 
    if (message.text == 'Воин'):
        hp += prof_database['Воин']['hp']
        damage+= prof_database['Воин']['damage']
        text = f'Вы неудержимый боец, а это значит, что ваше здоровье равно:{hp}, а урон равен:{damage}. Вперед к приключениям?'
        img = open('mech.jpg', 'rb')
        bot.send_photo(message.chat.id, img, caption = text, reply_markup = start_quest()) 
    if (message.text == 'Маг'):
        hp += prof_database['Маг']['hp']
        damage+= prof_database['Маг']['damage']
        text = f'Вы могущественный маг, а это значит, что ваше здоровье равно:{hp}, а урон равен:{damage}. Вперед к приключениям?'
        img = open('posoh.jpg', 'rb')
        bot.send_photo(message.chat.id, img, caption = text, reply_markup = start_quest()) 

    if (message.text == 'В путь!'):        
        event = random.randint(1,4)
        if event == 1 or event == 3 or event ==4:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button3 = 'В путь!'
            button4 = 'Вернуться в главное меню'
            markup.add(button3, button4)            
            bot.send_message(message.chat.id, text = "Пока никто не встретился... Идём дальше?" , reply_markup = markup)            
        elif event == 2:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button5 = 'Атаковать'
            button6 = 'Бежать'
            button7 = 'Вернуться в главное меню'
            #victim = create_monster()
            print(type(victim))
            markup.add(button5, button6, button7)
            bot.send_message(message.chat.id, text = f"Ого! Встретился монстр! Монстра зовут {victim[0]}, у него {victim[1]} очков здоровья и вот такой урон:{victim[2]} " , reply_markup = markup)
    if (message.text == 'Атаковать'):       
        victim[1] -= damage 
        print(victim[1])       
        if victim[1] <= 0:
            exp+=10 * lvl
            if exp >= lvl*30:
                lvl+=1
                hp+=25*lvl
                damage+=15*lvl
                bot.send_message(message.chat.id, text = f'Твой уровень повысился! \
Теперь у тебя {lvl} уровень. hp:{hp}, damage:{damage}')
            bot.send_message(message.chat.id, text = f'Враг повержен! За победу\
ты получаешь {10*lvl} очков опыта. Теперь у тебя: {exp} очков. Продожаем путешествие?', reply_markup = start_quest())
        elif victim[1] > 0:
            hp -= victim[2] 
            print(hp)
            bot.send_message(message.chat.id, text = f'Монстр атакаует!') 
            if hp <= 0:
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                button1 = 'Вернуться в главное меню'
                markup.add(button1)
                bot.send_message(message.chat.id, text = 'Победа осталась за монстром!', reply_markup = markup)
            elif hp > 0:
                bot.send_message(message.chat.id, text = f' Теперь у монстра {victim[1]} \
очков здоровья и {victim[2]} урон, а у тебя {hp} очков здоровья. Что будешь делать?', reply_markup = combat())
    elif (message.text == 'Бежать'):
        plan=random.randint(1,2)
        if plan==1:
            bot.send_message(message.chat.id, text = f'Вы сумели сбежать от монстра! Продожаем путешествие?', reply_markup = start_quest())
        elif plan==2:
            hp -= victim[2] 
            bot.send_message(message.chat.id, text = f'О ужас! Побег не удался и монстр атакаует!') 
            if hp <= 0:
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                button1 = 'Вернуться в главное меню'
                markup.add(button1)
                bot.send_message(message.chat.id, text = 'Победа осталась за монстром!', reply_markup = markup)
            elif hp > 0:
                bot.send_message(message.chat.id, text = f' Теперь у монстра {victim[1]} \
очков здоровья и {victim[2]} урон, а у тебя {hp} очков здоровья. Что будешь делать?', reply_markup = combat())
             
monster = ['Вася', 'Петя', 'Маша', 'Даша']
bot.polling(non_stop=True)



  
