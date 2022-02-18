import telebot
import random
from random import randint
import wikipedia
import re

wikipedia.set_lang("ru")

math = 0
koloda = []
count = 0
pravda = False
kostel = False

def y(message):
    global koloda
    global kostel
    global count
    if message.text.lower().find('y') != -1:
        current = koloda.pop()
        bot.send_message(message.chat.id, 'Будете брать карту ? /y и /n\n')
        count += current
        kostel = True
        if count > 21:
            bot.send_message(message.chat.id, 'Вы проиграли.')
            return False
        elif count == 21:
            bot.send_message(message.chat.id, 'Выпало 21, повезло.')
            return False
        else:
            bot.send_message(message.chat.id, 'У вас %d очков.' % count)
    else:
        bot.send_message(message.chat.id, 'У вас %d очков и вы закончили игру.' % count)
        return False

bot = telebot.TeleBot('5198146874:AAEJIBxddzOHXPrXuW6mRbRZT070bvcfIIg')

@bot.message_handler(commands=['start'])
def start(message, res=False):
    bot.send_message(message.chat.id, 'Доброго времени суток, это личный бот N.K.\nКоманда /help расскажет о функционале бота.\nБот выполнен 18.02.2022 в 0:25 для мтуси.')

@bot.message_handler(commands=["help"])
def helpa(message):
    bot.send_message(message.chat.id,'Мой список команд:\n1.Игра в 21, чтобы сыграть вызовите /play.\n2.Проверка ваших умственных способностей, чтобы проверить вызовите /calc.\n3.Если написать /wiki <поисковой запрос>, то выведет краткую информацию из вики.\n4.Ссылка на лучший сайт на планете /url')

@bot.message_handler(commands=["play"])
def handle_text(message):
    global count
    global kostel
    global koloda
    bot.send_message(message.chat.id,'Пошла игра..., взять карту /y, пас - /n')
    count = 0
    koloda = [6, 7, 8, 9, 10, 2, 3, 4, 11] * 4
    random.shuffle(koloda)
    kostel = True

@bot.message_handler(commands=["url"])
def handle_text(message):
    bot.send_message(message.chat.id, "Ссылка - mtuci.ru")

@bot.message_handler(commands=["calc"])
def handle_text(message):
    global math
    global pravda
    a = randint(1,100)
    b = randint(1,100)
    c = randint(1,2)
    if c == 1:
        math = a + b
        bot.send_message(message.chat.id, f'Решика мне, а я проверю ... {a}+{b} = ?.')
    else:
        math = a - b
        bot.send_message(message.chat.id, f'Решика мне, а я проверю ... {a}-{b} = ?.')
    pravda = True

def wiki(s):
    try:
        pervya1000 = wikipedia.page(s)
        wikitext = pervya1000.content[:1000]
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitextfinal = ''
        for x in wikimas:
            if not('==' in x):
                if(len((x.strip()))>3):
                    wikitextfinal=wikitextfinal+x+'.'
            else:
                break
        wikitextfinal = re.sub('\([^()]*\)', '', wikitextfinal)
        wikitextfinal = re.sub('\([^()]*\)', '', wikitextfinal)
        wikitextfinal = re.sub('\{[^\{\}]*\}', '', wikitextfinal)
        return wikitextfinal
    except Exception as e:
        return 'Не могу найти информацию на ваше слово'

@bot.message_handler(content_types=['text'])
def answer(message):
    global kostel
    global pravda
    msg = message.text.lower()
    if kostel == True:
        kostel = False
        if msg == '/y' or '/n':
            t = y(message)
            if t == False:
                global koloda
                koloda = 0
                global count
                count = 0
                bot.send_message(message.chat.id, 'Вы закончили игру, можете вернуться в начало - /play.')
    if pravda == True:
        pravda = False
        if msg == str(math):
            bot.send_message(message.chat.id, 'Вау, ты закончил приходскую школу, можете вернуться в начало - /calc.')
        else:
            bot.send_message(message.chat.id, 'К сожалению, вам пора в армию, можете вернуться в начало - /calc.')
    if msg.find("gym?") != -1:
        bot.send_message(message.chat.id, 'GYM - это империя.')
    if msg.find("как дела?") != -1:
        bot.send_message(message.chat.id, 'это новый кадилак')
    if msg.find("кто выиграл чкг?") != -1:
        bot.send_message(message.chat.id, 'GYM!\nGYM!\nGYM!')
    if msg.find('/wiki') != -1:
        s = msg.replace('/wiki', '', 1)
        bot.send_message(message.chat.id, wiki(s[1:]))

bot.polling(none_stop=True, interval=0)

