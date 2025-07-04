from telebot.types import Message
import telebot
import requests

API_URL = "http://127.0.0.1:8000/api"
BOT_TOKEN = "7781641058:AAHZ1-gHQrZvSxYk-murPvIR1gwyomiCQLw"

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
    data = {
        "user_id": message.from_user.id,
        "username": message.from_user.username
    }
    response = requests.post(API_URL + "/register/", json=data)
    if not response.status_code == 200:
        if response.json().get('message'):
            bot.send_message(message.chat.id, "Вы уже были зарегистрированы ранее!")
        else:
            bot.send_message(message.chat.id,
                             f"Вы успешно зарегистрированы! Ваш уникальный номер: {response.json()['id']}")
    else:
        bot.send_message(message.chat.id, f"Произошла ошибка ри регистрации!")
        print(response.json())
        print(response.status_code)
        print(response.text)


if __name__ == "__main__":
    bot.polling(none_stop=True)