from telebot import TeleBot
import requests
import json
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
    msg = bot.send_message(chat_id = chat_id, text = f'{first_name}, введите название города: ')

    bot.register_next_step_handler(msg, rely_to_user)
        
def get_weather_name_by_city(city_name):
    parameters = {
        'appid' : 'ee266eda7e1fd71ccc7fab28b894385b',
        'units' : 'metric',
        'lang' : 'ru',
        'q' : city_name 
    }

    response = requests.get('http://api.openweathermap.org/data/2.5/weather', parameters)
    data = response.json()
    
    try:
        message = f'''В городе <b>{data['name']}</b>: 
<i>{data['weather'][0]['description'].capitalize()}</i>
Температура воздуха {data['main']['temp']} градусов по Цельсию,
Скорость ветра {data['wind']['speed']} м/с.''' 
    except KeyError:
        message = 'Такого города не существует'

    return message

def rely_to_user(message):
    chat_id = message.chat.id
    user_text = message.text

    if user_text.lower() in unswers:
        bot.send_message(chat_id, 'Бот остановлен, для возобновления нажмите команду /start ')
        return

    message_to_user = get_weather_name_by_city(user_text)

    msg = bot.reply_to(message, message_to_user, parse_mode='HTML')
    bot.register_next_step_handler(msg, rely_to_user)

print('Бот работает')
bot.polling()