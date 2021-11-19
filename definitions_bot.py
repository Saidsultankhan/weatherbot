from telebot import TeleBot
import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint

token = '1813626382:AAGf8b3IO4Vl8wZgYWfpnhBaGnZ-d62P69A'

bot = TeleBot(token)

unswers = ['stop', 'стоп', '/stop']

@bot.message_handler(commands=['start', 'help']) 
def command_start(message):
    chat_id = message.chat.id
    first_name = message.chat.first_name

    bot.send_message(chat_id, f'Hi, {first_name}!')
    insert_city_name(message)

def insert_city_name(message):
    chat_id = message.chat.id
    first_name = message.chat.first_name.capitalize()
    
    bot.send_message(chat_id, 'Чтобы остановить бота, нажмите на /stop ')
    msg = bot.send_message(chat_id = chat_id, text = f'{first_name}, введите слово: ')

    bot.register_next_step_handler(msg, rely_to_user)
        
def get_definition(word):
    
    try:
        req = requests.get(f'https://www.merriam-webster.com/dictionary/{word}')
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        translate = soup.find('span', class_='dtText')
        message = translate.get_text(strip=True)
    except KeyError:
        message = 'Такого города не существует'

    return f'{word} {message}'

def rely_to_user(message):
    chat_id = message.chat.id
    user_text = message.text

    if user_text.lower() in unswers:
        bot.send_message(chat_id, 'Бот остановлен, для возобновления нажмите команду /start ')
        return

    message_to_user = get_definition(user_text)

    msg = bot.reply_to(message, message_to_user)
    bot.register_next_step_handler(msg, rely_to_user)

print('Бот работает')
bot.polling()